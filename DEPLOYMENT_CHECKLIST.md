# Deployment checklist

1. Work on lowercase `develop`; keep `main` untouched.
2. Create venv, install requirements, create local `.env` from `.env.example`.
3. Keep `LIVE_TRADING=false`.
4. Run `chmod +x bot && ./bot test`.
5. Configure the real WebSocket URL/auth only in `.env`.
6. Run `./bot capture` to capture exactly one real message without loading Dhan execution.
7. Map the captured schema into normalization/parser logic.
8. Verify current Dhan order API and instrument-master schema before implementing broker execution.
9. Implement/test equity resolution, then exact F&O expiry/strike/lot/tick resolution.
10. Add Telegram commands/status and restart recovery checks.
11. Install systemd only after all no-order tests pass.
12. Enable live trading only for a controlled broker test after the execution path is reviewed.
