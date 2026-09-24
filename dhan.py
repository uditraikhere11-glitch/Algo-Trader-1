class DhanBroker:
    """Dhan execution boundary.

    Order placement remains locked until current Dhan API fields, instrument mapping,
    and the captured upstream WebSocket schema are verified.
    """
    def __init__(self, client_id: str = "", access_token: str = ""):
        self.client_id = client_id
        self.access_token = access_token

    async def execute(self, signal):
        raise RuntimeError("LIVE_EXECUTION_NOT_CONFIGURED")
