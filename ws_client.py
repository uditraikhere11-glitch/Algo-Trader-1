from collections.abc import AsyncIterator
import websockets


def websocket_headers(token: str) -> dict[str, str] | None:
    return {"Authorization": f"Bearer {token}"} if token else None


async def connect_messages(url: str, token: str = "") -> AsyncIterator[str | bytes]:
    if not url:
        raise RuntimeError("WEBSOCKET_URL is required")
    async with websockets.connect(
        url,
        additional_headers=websocket_headers(token),
        ping_interval=20,
        ping_timeout=20,
        close_timeout=10,
    ) as ws:
        async for raw in ws:
            yield raw
