from typing import Dict, Optional, List
from app.config import AppConfig

class AlertService:
    def __init__(self, config: AppConfig):
        self.config = config

    def check_alerts(self, prices):
        triggered = []

        for coin in self.config.coins:
            price = prices.get(coin.id)

            if price is None:
                continue

            for alert in coin.alerts:
                alert_type = alert.get("type")
                value = alert.get("value")

                # значки крипты
                icon = self._get_icon(coin.symbol)

                if alert_type == "above" and price >= value:
                    message = (
                        f"{icon} {coin.symbol} price ABOVE {value}\n\n"
                        f"Current price {coin.symbol}: {price} USD"
                    )
                    triggered.append(message)

                elif alert_type == "below" and price <= value:
                    message = (
                        f"{icon} {coin.symbol} price BELOW {value}\n\n"
                        f"Current price {coin.symbol}: {price} USD"
                    )
                    triggered.append(message)

        return triggered
    
    def _get_icon(self, symbol: str) -> str:
        icons = {
            "BTC": "₿",
            "ETH": "Ξ",
            "LTC": "Ł",
            "TIA": "🔹"
        }
        return icons.get(symbol, "💰")