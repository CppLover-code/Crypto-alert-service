import aiohttp
import asyncio
import smtplib
from email.mime.text import MIMEText
from typing import Optional


class TelegramNotifier:
    def __init__(self, token: str):
        self.token = (token or "").strip()
        self.base_url = f"https://api.telegram.org/bot{self.token}"
        self.session: Optional[aiohttp.ClientSession] = None

    async def start(self):
        """Initialize HTTP session"""
        self.session = aiohttp.ClientSession()

    async def close(self):
        """Close HTTP session"""
        if self.session:
            await self.session.close()

    async def send_message(self, text: str, chat_id: str):
        if not self.session:
            raise RuntimeError(
                "Telegram session is not initialized. Call start()."
            )

        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": int(chat_id) if str(chat_id).isdigit() else chat_id,
            "text": text
        }

        async with self.session.post(url, json=payload) as response:
            body = await response.text()
            if response.status != 200:
                raise RuntimeError(
                    f"Failed to send Telegram message: "
                    f"{response.status} - {body}"
                )
            if '"ok":false' in body.replace(" ", "").lower():
                raise RuntimeError(
                    f"Telegram API rejected the message: {body}"
                )


class EmailNotifier:
    def __init__(self, config):
        self.config = config

    async def send_email(self, subject: str, body: str, to_email: str):
        await asyncio.to_thread(
            self._send_email_sync,
            subject,
            body,
            to_email,
        )

    def _send_email_sync(self, subject: str, body: str, to_email: str):
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = self.config.sender_email
        msg["To"] = to_email

        with smtplib.SMTP(
            self.config.smtp_server,
            self.config.smtp_port
        ) as server:
            server.starttls()
            server.login(
                self.config.sender_email,
                self.config.app_password
            )
            server.send_message(msg)
