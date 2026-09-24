import asyncio
import tempfile
from pathlib import Path

from state import StateStore
from trading_engine import TradingEngine, normalize_signal


def test_equity_normalize():
    s = normalize_signal({"signal_id":"abc","symbol":"YESBANK","side":"BUY","segment":"EQUITY","qty":1})
    assert s.symbol == "YESBANK" and s.quantity == 1


def test_nested_payload():
    s = normalize_signal({"data":{"id":"x1","scrip":"RELIANCE","action":"BUY"}})
    assert s.signal_id == "x1" and s.symbol == "RELIANCE"


def test_non_buy_blocked():
    try:
        normalize_signal({"id":"x","symbol":"ABC","side":"SELL"})
    except ValueError:
        return
    assert False


def test_dedupe_and_last_signal():
    with tempfile.TemporaryDirectory() as d:
        st = StateStore(f"{d}/x.db")
        assert st.record("one", {"id":"one"}) is True
        assert st.record("one", {"id":"one"}) is False
        assert st.seen("one")
        assert st.last_signal()["signal_id"] == "one"


def test_live_false_never_calls_broker():
    class Broker:
        async def execute(self, signal):
            raise AssertionError("broker must not be called")
    s = normalize_signal({"id":"safe","symbol":"ABC","side":"BUY"})
    result = asyncio.run(TradingEngine(Broker(), live=False).execute(s))
    assert result["status"] == "BLOCKED"


def test_capture_module_has_no_dhan_import():
    text = Path("capture_ws.py").read_text(encoding="utf-8")
    assert "from dhan" not in text and "import dhan" not in text
