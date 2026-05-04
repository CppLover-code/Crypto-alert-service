import json
from pathlib import Path
from typing import List, Optional

class CoinConfig:
    def __init__(self, data: dict):
        self.id: str = data["id"]
        self.symbol: str = data["symbol"]
        self.threshold: Optional[float] = data.get("threshold")


class APIConfig:
    def __init__(self, data: dict):
        self.base_url: str = data["base_url"]
        self.timeout: int = data("timeout", 5)
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


def load_config(path: str = "config/config.json") -> AppConfig:
    config_path = Path(path)

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(config_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return AppConfig(data)