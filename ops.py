import aiohttp
import logging

log = logging.getLogger(__name__)

class TelegramOps:
    def __init__(self, token: str = "", chat_id: str = ""):
        self.token = token.strip()
        self.chat_id = chat_id.strip()

    async def notify(self, text: str) -> None:
        if not self.token or not self.chat_id:
            return
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        try:
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(url, json={"chat_id": self.chat_id, "text": text}) as response:
                    if response.status >= 400:
                        log.error("Telegram notify failed HTTP %s", response.status)
        except Exception:
            log.exception("Telegram notify failed")
