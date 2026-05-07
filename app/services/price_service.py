from datetime import datetime, UTC
from typing import Dict
from app.api.client import CoinGeckoClient
from app.config import AppConfig


class PriceService:
    def __init__(self, client: CoinGeckoClient, config: AppConfig):
        self.client = client
        self.config = config

    async def fetch_prices(self) -> Dict[str, object]:
        # берём монеты из config
        coins = [coin.id for coin in self.config.coins]

        # вызываем API
        prices = await self.client.get_prices(coins)

        # добавляем timestamp
        result = {
            "timestamp": datetime.now().isoformat(),
            "prices": prices
        }

        return result