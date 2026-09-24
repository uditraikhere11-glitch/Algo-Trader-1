# Deployment checklist

1. Upload/extract this repository on the `Develop` branch.
2. Create a Python venv and install `requirements.txt`.
3. Copy `.env.example` to `.env`; never commit `.env`.
4. Keep `LIVE_TRADING=false`.
5. Run `chmod +x bot && ./bot test`.
6. Configure the real WebSocket URL/auth.
7. Capture one real incoming payload and finalize normalization.
8. Verify current Dhan API/order fields and instrument master before implementing live execution.
9. Test equity and F&O resolution without live placement.
10. Configure systemd only after the above checks pass.
