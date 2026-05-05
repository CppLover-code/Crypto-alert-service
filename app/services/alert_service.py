from typing import Dict, Optional, List
from app.config import AppConfig

class AlertService:
    def __init__(self, config: AppConfig):
        self.config = config

    def check_alerts(self, prices: Dict[str, Optional[float]]) -> List[str]:
       # Проверяет условия и возвращает монеты, где превышен threshold

        triggered = []

        for coin in self.config.coins:
            price = prices.get(coin.id)

            if price is None:
                continue

            for alert in coin.alerts:
                alert_type = alert.get("type")
                value = alert.get("value")

                if alert_type == "above" and price >= value:
                    triggered.append(
                        f"{coin.symbol}: price {price} >= {value}"
                    )

                elif alert_type == "below" and price <= value:
                    triggered.append(
                        f"{coin.symbol}: price {price} <= {value}"
                    )

        return triggered