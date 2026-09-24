"""Capture exactly one raw WebSocket message. This module imports no broker code."""
import asyncio
from pathlib import Path
from config import Settings
from ws_client import connect_messages


async def capture_one() -> Path:
    settings = Settings.from_env()
    target = Path(settings.capture_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    async for raw in connect_messages(settings.websocket_url, settings.websocket_auth_token):
        data = raw.decode("utf-8", errors="replace") if isinstance(raw, bytes) else raw
        target.write_text(data, encoding="utf-8")
        return target
    raise RuntimeError("WebSocket closed before a message was received")


if __name__ == "__main__":
    path = asyncio.run(capture_one())
    print(f"Captured one raw WebSocket message to {path}")
    print("No Dhan broker code was loaded; no order can be placed by this command.")
