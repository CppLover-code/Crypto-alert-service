from typing import Dict, Optional
from app.config import AppConfig

class AlertService:
    def __init__(self, config: AppConfig):
        self.config = config

    def check_alerts(self, prices: Dict[str, Optional[float]]) -> Dict[str, float]: 
       # Проверяет условия и возвращает монеты, где превышен threshold

        triggered = {}

        for coin in self.config.coins:
            price = prices.get(coin.id)

            if price is None:
                continue

            if coin.threshold is not None and price >= coin.threshold:
                triggered[coin.id] = price

        return triggered