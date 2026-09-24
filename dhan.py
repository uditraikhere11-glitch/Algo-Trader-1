class DhanBroker:
    """Dhan execution boundary. Live placement stays locked until API/order mapping is verified."""
    def __init__(self, client_id: str = "", access_token: str = ""):
        self.client_id = client_id
        self.access_token = access_token

    async def execute(self, signal):
        raise RuntimeError("LIVE_EXECUTION_NOT_CONFIGURED: verify Dhan API mapping before enabling")
