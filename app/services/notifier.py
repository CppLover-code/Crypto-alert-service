import aiohttp
import smtplib
from email.mime.text import MIMEText


class TelegramNotifier:
    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id

    async def send_message(self, text: str):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"

        payload = {
            "chat_id": self.chat_id,
            "text": text
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status != 200:
                    raise RuntimeError("Failed to send Telegram message")
                
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