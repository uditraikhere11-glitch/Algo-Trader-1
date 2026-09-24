import json
import sqlite3
from pathlib import Path
from typing import Any


class StateStore:
    def __init__(self, path: str):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(path)
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("""CREATE TABLE IF NOT EXISTS signals(
            signal_id TEXT PRIMARY KEY,
            received_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            status TEXT NOT NULL,
            payload TEXT NOT NULL,
            error TEXT
        )""")
        self.conn.commit()

    def seen(self, signal_id: str) -> bool:
        return self.conn.execute("SELECT 1 FROM signals WHERE signal_id=?", (signal_id,)).fetchone() is not None

    def record(self, signal_id: str, payload: dict[str, Any], status: str = "RECEIVED") -> bool:
        cur = self.conn.execute(
            "INSERT OR IGNORE INTO signals(signal_id,status,payload) VALUES(?,?,?)",
            (signal_id, status, json.dumps(payload, separators=(",", ":"), default=str)),
        )
        self.conn.commit()
        return cur.rowcount == 1

    def set_status(self, signal_id: str, status: str, error: str | None = None) -> None:
        self.conn.execute(
            "UPDATE signals SET status=?, error=?, updated_at=CURRENT_TIMESTAMP WHERE signal_id=?",
            (status, error, signal_id),
        )
        self.conn.commit()

    def last_signal(self) -> dict[str, Any] | None:
        row = self.conn.execute(
            "SELECT signal_id,received_at,updated_at,status,payload,error FROM signals ORDER BY received_at DESC LIMIT 1"
        ).fetchone()
        if not row:
            return None
        return {"signal_id": row[0], "received_at": row[1], "updated_at": row[2], "status": row[3],
                "payload": json.loads(row[4]), "error": row[5]}

    def close(self) -> None:
        self.conn.close()
