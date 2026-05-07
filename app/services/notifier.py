import aiohttp
import smtplib
from email.mime.text import MIMEText
from typing import Optional


class TelegramNotifier:
    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id

        self.base_url = f"https://api.telegram.org/bot{token}"

        self.session: Optional[aiohttp.ClientSession] = None

    async def start(self):
        """Initialize HTTP session"""
        self.session = aiohttp.ClientSession()

    async def close(self):
        """Close HTTP session"""
        if self.session:
            await self.session.close()

    async def send_message(self, text: str):

        if not self.session:
            raise RuntimeError(
                "Telegram session is not initialized. Call start()."
            )

        url = f"{self.base_url}/sendMessage"

        payload = {
            "chat_id": self.chat_id,
            "text": text
        }

        async with self.session.post(url, json=payload) as response:

            if response.status != 200:
                response_text = await response.text()

                raise RuntimeError(
                    f"Failed to send Telegram message: "
                    f"{response.status} - {response_text}"
                )
                
class EmailNotifier:
    def __init__(self, config):
        self.config = config

    def send_email(self, subject: str, body: str):
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = self.config.sender_email
        msg["To"] = self.config.receiver_email

        try:
            with smtplib.SMTP(self.config.smtp_server, self.config.smtp_port) as server:
                server.starttls()
                server.login(self.config.sender_email, self.config.app_password)
                server.send_message(msg)

        except Exception as e:
            print(f"Email error: {e}")