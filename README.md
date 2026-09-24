# Algo-Trader-1

External WebSocket → validation/normalization → SQLite dedupe/recovery → trading engine → Dhan.
Telegram Bot API is monitoring/operations only; it is not the trade-signal source.

## Current milestone
The transport, state journal, duplicate protection, safe capture utility, monitoring boundary, and execution gate are implemented. Dhan live placement and exact F&O resolution remain intentionally locked until the actual upstream WebSocket payload and current Dhan API/instrument schema are verified.

## Safe first run
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env
chmod +x bot
./bot test
./bot capture
```

`./bot capture` receives exactly one raw upstream WebSocket message and writes it to `runtime/captured_ws_payload.txt`. It imports no Dhan broker module and cannot place an order.

Never commit `.env`, broker credentials, Telegram tokens, captured runtime payloads, or SQLite databases.
