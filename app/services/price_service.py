from datetime import datetime
from typing import Dict, Any

from app.api.client import CoinGeckoClient
from app.config import AppConfig


class PriceService:
    def __init__(self, client: CoinGeckoClient, config: AppConfig):
        self.client = client
        self.config = config

    async def fetch_prices(self) -> Dict[str, Any]:
        """
        Получает цены и возвращает структурированный результат
        """

        # берём монеты из config
        coins = [coin.id for coin in self.config.coins]

        # вызываем API
        prices = await self.client.get_prices(coins)

        # добавляем timestamp
        result = {
            "timestamp": datetime.utcnow().isoformat(),
            "prices": prices
        }

        return result