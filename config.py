import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

def env_bool(name: str, default: bool = False) -> bool:
    return os.getenv(name, str(default)).strip().lower() in {"1", "true", "yes", "on"}

@dataclass(frozen=True)
class Settings:
    websocket_url: str
    websocket_auth_token: str
    live_trading: bool
    db_path: str
    capture_path: str
    dhan_client_id: str
    dhan_access_token: str
    telegram_bot_token: str
    telegram_chat_id: str
    log_level: str

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            websocket_url=os.getenv("WEBSOCKET_URL", "").strip(),
            websocket_auth_token=os.getenv("WEBSOCKET_AUTH_TOKEN", "").strip(),
            live_trading=env_bool("LIVE_TRADING", False),
            db_path=os.getenv("DB_PATH", "runtime/darvas.db").strip(),
            capture_path=os.getenv("CAPTURE_PATH", "runtime/captured_ws_payload.txt").strip(),
            dhan_client_id=os.getenv("DHAN_CLIENT_ID", "").strip(),
            dhan_access_token=os.getenv("DHAN_ACCESS_TOKEN", "").strip(),
            telegram_bot_token=os.getenv("TELEGRAM_BOT_TOKEN", "").strip(),
            telegram_chat_id=os.getenv("TELEGRAM_CHAT_ID", "").strip(),
            log_level=os.getenv("LOG_LEVEL", "INFO").strip().upper(),
        )
