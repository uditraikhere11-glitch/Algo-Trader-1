from dataclasses import dataclass

@dataclass(frozen=True)
class Instrument:
    security_id: str
    symbol: str
    segment: str
    lot_size: int = 1
    tick_size: float = 0.05

class InstrumentResolver:
    """Boundary for Dhan master and exact F&O contract resolution."""
    def resolve(self, symbol: str, segment: str) -> Instrument:
        raise LookupError(f"Instrument master not loaded for {segment}:{symbol}")
