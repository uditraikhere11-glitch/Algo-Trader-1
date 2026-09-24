import asyncio, json, logging, os
import websockets
from dotenv import load_dotenv
from dhan import DhanBroker
from ops import TelegramOps
from state import StateStore
from trading_engine import TradingEngine, normalize_signal

load_dotenv()
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), format="%(asctime)s %(levelname)s %(name)s %(message)s")
log = logging.getLogger("algo-trader")

def env_bool(name: str, default: bool = False) -> bool:
    return os.getenv(name, str(default)).lower() in {"1", "true", "yes", "on"}

async def run():
    ws_url = os.getenv("WEBSOCKET_URL", "").strip()
    if not ws_url: raise RuntimeError("WEBSOCKET_URL is required")
    live = env_bool("LIVE_TRADING", False)
    store = StateStore(os.getenv("DB_PATH", "runtime/darvas.db"))
    ops = TelegramOps(os.getenv("TELEGRAM_BOT_TOKEN", ""), os.getenv("TELEGRAM_CHAT_ID", ""))
    broker = DhanBroker(os.getenv("DHAN_CLIENT_ID", ""), os.getenv("DHAN_ACCESS_TOKEN", ""))
    engine = TradingEngine(broker, live=live)
    headers = {}
    token = os.getenv("WEBSOCKET_AUTH_TOKEN", "").strip()
    if token: headers["Authorization"] = f"Bearer {token}"
    await ops.notify(f"BOT STARTED | live={live}")
    delay = 2
    while True:
        try:
            async with websockets.connect(ws_url, additional_headers=headers or None, ping_interval=20, ping_timeout=20) as ws:
                delay = 2; log.info("WEBSOCKET CONNECTED"); await ops.notify("WEBSOCKET CONNECTED")
                async for raw in ws:
                    log.info("[SIGNAL] Received")
                    try:
                        payload = json.loads(raw)
                        if not isinstance(payload, dict): raise ValueError("payload must be JSON object")
                        signal = normalize_signal(payload)
                        if store.seen(signal.signal_id):
                            log.info("[BLOCKED] DUPLICATE %s", signal.signal_id); continue
                        store.record(signal.signal_id, payload)
                        log.info("[EXECUTING] %s %s", signal.segment, signal.symbol)
                        result = await engine.execute(signal)
                        store.set_status(signal.signal_id, result.get("status", "UNKNOWN"))
                        await ops.notify(f"{result.get('status')} | {signal.segment} | {signal.symbol} | {signal.signal_id}")
                    except Exception as exc:
                        log.exception("[ERROR] processing signal"); await ops.notify(f"EXECUTION ERROR | {type(exc).__name__}: {exc}")
        except asyncio.CancelledError: raise
        except Exception as exc:
            log.warning("WEBSOCKET DISCONNECTED: %s; reconnecting in %ss", exc, delay)
            await ops.notify(f"WEBSOCKET DISCONNECTED | reconnect in {delay}s")
            await asyncio.sleep(delay); delay = min(delay * 2, 60)

if __name__ == "__main__": asyncio.run(run())
