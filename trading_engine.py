import logging
from dataclasses import dataclass
from typing import Any

log = logging.getLogger(__name__)

@dataclass(frozen=True)
class Signal:
    signal_id: str
    segment: str
    symbol: str
    side: str
    quantity: int | None
    raw: dict[str, Any]

def normalize_signal(payload: dict[str, Any]) -> Signal:
    body = payload.get("data", payload)
    if not isinstance(body, dict):
        raise ValueError("signal body must be an object")
    sid = str(body.get("signal_id") or body.get("id") or "").strip()
    symbol = str(body.get("symbol") or body.get("scrip") or "").strip().upper()
    side = str(body.get("side") or body.get("action") or "BUY").strip().upper()
    segment = str(body.get("segment") or body.get("type") or "EQUITY").strip().upper()
    qty = body.get("quantity", body.get("qty"))
    if not sid: raise ValueError("missing signal_id/id")
    if not symbol: raise ValueError("missing symbol/scrip")
    if side != "BUY": raise ValueError("buy-only safety policy blocked non-BUY signal")
    if qty is not None:
        qty = int(qty)
        if qty <= 0: raise ValueError("quantity must be positive")
    return Signal(sid, segment, symbol, side, qty, payload)

class TradingEngine:
    def __init__(self, broker, live: bool = False):
        self.broker = broker
        self.live = live

    async def execute(self, signal: Signal) -> dict[str, Any]:
        if not self.live:
            log.warning("[BLOCKED] LIVE_TRADING=false signal=%s", signal.signal_id)
            return {"status": "BLOCKED", "reason": "LIVE_TRADING=false"}
        return await self.broker.execute(signal)
