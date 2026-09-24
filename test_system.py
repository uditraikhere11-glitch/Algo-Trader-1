import tempfile
from state import StateStore
from trading_engine import normalize_signal

def test_equity_normalize():
    s=normalize_signal({"signal_id":"abc","symbol":"YESBANK","side":"BUY","segment":"EQUITY","qty":1})
    assert s.symbol=="YESBANK" and s.quantity==1

def test_nested_payload():
    s=normalize_signal({"data":{"id":"x1","scrip":"RELIANCE","action":"BUY"}})
    assert s.signal_id=="x1" and s.symbol=="RELIANCE"

def test_non_buy_blocked():
    try: normalize_signal({"id":"x","symbol":"ABC","side":"SELL"})
    except ValueError: return
    assert False

def test_dedupe():
    with tempfile.TemporaryDirectory() as d:
        st=StateStore(f"{d}/x.db"); st.record("one", {"id":"one"}); assert st.seen("one")
