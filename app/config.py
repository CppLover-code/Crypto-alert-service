import json
from pathlib import Path
from typing import List, Optional

class TelegramConfig:
    def __init__(self, data: dict):
        self.enabled: bool = data.get("enabled", False)
        self.bot_token: str = data["bot_token"]
        self.chat_id: str = data["chat_id"]

class CoinConfig:
    def __init__(self, data: dict):
        self.id: str = data["id"]
        self.symbol: str = data["symbol"]
        self.alerts = data.get("alerts", [])

class AlertsConfig:
    def __init__(self, data: dict):
        self.state_file: str = data.get("state_file", "data/alerts_state.json")

class APIConfig:
    def __init__(self, data: dict):
        self.base_url: str = data["base_url"]
        self.timeout: int = data.get("timeout", 5)
        self.max_retries: int = data.get("max_retries", 3)

class StorageConfig:
    def __init__(self, data: dict):
        self.file_path: str = data["file_path"]


class LoggingConfig:
    def __init__(self, data: dict):
        self.level: str = data.get("level", "INFO")
        self.file_path: str = data["file_path"]


class AppConfig:
    def __init__(self, data: dict):
        self.interval_seconds: int = data.get("interval_seconds", 60)
        self.api = APIConfig(data["api"])
        self.coins: List[CoinConfig] = [CoinConfig(c) for c in data["coins"]]
        self.storage = StorageConfig(data["storage"])
        self.logging = LoggingConfig(data["logging"])
        notifications = data.get("notifications", {})
        self.telegram = TelegramConfig(notifications.get("telegram", {}))
        self.alerts = AlertsConfig(data.get("alerts", {}))


def load_config(path: str = "config/config.json") -> AppConfig:
    config_path = Path(path)

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(config_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return AppConfig(data)