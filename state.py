import json
import sqlite3
from pathlib import Path
from typing import Any

class StateStore:
    def __init__(self, path: str):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(path)
        self.conn.execute("""CREATE TABLE IF NOT EXISTS signals(
            signal_id TEXT PRIMARY KEY,
            received_at TEXT DEFAULT CURRENT_TIMESTAMP,
            status TEXT NOT NULL,
            payload TEXT NOT NULL,
            error TEXT
        )""")
        self.conn.commit()

    def seen(self, signal_id: str) -> bool:
        return self.conn.execute("SELECT 1 FROM signals WHERE signal_id=?", (signal_id,)).fetchone() is not None

    def record(self, signal_id: str, payload: dict[str, Any], status: str = "RECEIVED") -> None:
        self.conn.execute("INSERT OR IGNORE INTO signals(signal_id,status,payload) VALUES(?,?,?)",
                          (signal_id, status, json.dumps(payload, separators=(",", ":"), default=str)))
        self.conn.commit()

    def set_status(self, signal_id: str, status: str, error: str | None = None) -> None:
        self.conn.execute("UPDATE signals SET status=?, error=? WHERE signal_id=?", (status, error, signal_id))
        self.conn.commit()
