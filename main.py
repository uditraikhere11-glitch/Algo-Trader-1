import asyncio
import json
import logging

from config import Settings
from dhan import DhanBroker
from ops import TelegramOps
from state import StateStore
from trading_engine import TradingEngine, normalize_signal
from ws_client import connect_messages


async def run() -> None:
    settings = Settings.from_env()
    logging.basicConfig(level=getattr(logging, settings.log_level, logging.INFO),
                        format="%(asctime)s %(levelname)s %(name)s %(message)s")
    log = logging.getLogger("algo-trader")
    if not settings.websocket_url:
        raise RuntimeError("WEBSOCKET_URL is required")

    store = StateStore(settings.db_path)
    ops = TelegramOps(settings.telegram_bot_token, settings.telegram_chat_id)
    broker = DhanBroker(settings.dhan_client_id, settings.dhan_access_token)
    engine = TradingEngine(broker, live=settings.live_trading)
    await ops.notify(f"BOT STARTED | live={settings.live_trading}")

    delay = 2
    while True:
        try:
            connected = False
            async for raw in connect_messages(settings.websocket_url, settings.websocket_auth_token):
                if not connected:
                    connected = True
                    delay = 2
                    log.info("WEBSOCKET CONNECTED")
                    await ops.notify("WEBSOCKET CONNECTED")
                try:
                    text = raw.decode("utf-8", errors="replace") if isinstance(raw, bytes) else raw
                    payload = json.loads(text)
                    if not isinstance(payload, dict):
                        raise ValueError("payload must be JSON object")
                    signal = normalize_signal(payload)
                    if store.seen(signal.signal_id):
                        log.info("[BLOCKED] DUPLICATE %s", signal.signal_id)
                        continue
                    store.record(signal.signal_id, payload)
                    log.info("[SIGNAL] %s %s %s", signal.signal_id, signal.segment, signal.symbol)
                    try:
                        result = await engine.execute(signal)
                    except Exception as exc:
                        store.set_status(signal.signal_id, "ERROR", str(exc))
                        raise
                    store.set_status(signal.signal_id, result.get("status", "UNKNOWN"))
                    await ops.notify(f"{result.get('status')} | {signal.segment} | {signal.symbol} | {signal.signal_id}")
                except Exception as exc:
                    log.exception("[ERROR] processing signal")
                    await ops.notify(f"EXECUTION ERROR | {type(exc).__name__}: {exc}")
            raise ConnectionError("WebSocket closed")
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            log.warning("WEBSOCKET DISCONNECTED: %s; reconnecting in %ss", exc, delay)
            await ops.notify(f"WEBSOCKET DISCONNECTED | reconnect in {delay}s")
            await asyncio.sleep(delay)
            delay = min(delay * 2, 60)


if __name__ == "__main__":
    asyncio.run(run())
