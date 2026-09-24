# Algo-Trader-1

WebSocket → validation/dedup → trading engine → Dhan framework.

## Current safety state
Live execution is intentionally locked. Keep `LIVE_TRADING=false` until the real WebSocket payload, current Dhan order fields, and instrument/F&O mapping are verified.

## Architecture
External WebSocket → `main.py` → normalization → SQLite dedupe/recovery → `TradingEngine` → Dhan boundary.

Telegram is operations/monitoring only, not a signal source.

## VM quick start
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env
./bot test
```

Secrets and runtime state (`.env`, SQLite DB, runtime files) are excluded from Git.
