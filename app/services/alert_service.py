import json
from pathlib import Path
from decimal import Decimal
from typing import Dict, List

class AlertService:
    def __init__(self, config):
        self.config = config
        self.state_file = Path(config.alerts.state_file)
        self.triggered_alerts = self._load_state()

    def _load_state(self):
        if not self.state_file.exists():
            return set()

        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except json.JSONDecodeError:
            return set()

    def _save_state(self):
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(list(self.triggered_alerts), f, indent=4)

    def check_alerts(self, prices: Dict[str, Decimal]) -> List[str]:
        triggered = []

        for coin in self.config.coins:
            price = prices.get(coin.id)

            if price is None:
                continue

            for alert in coin.alerts:
                alert_type = alert.get("type")
                value = Decimal(str(alert.get("value")))

                alert_key = f"{coin.id}_{alert_type}_{value}"

                icon = self._get_icon(coin.symbol)

                condition_met = False

                if alert_type == "above" and price >= value:
                    condition_met = True

                elif alert_type == "below" and price <= value:
                    condition_met = True

                # если условие выполнено
                if condition_met:
                    if alert_key not in self.triggered_alerts:

                        formatted_price = price.quantize(Decimal("0.01"))
                        formatted_value = value.quantize(Decimal("0.01"))

                        message = (
                            f"🚨 {icon} {coin.symbol} price {alert_type.upper()} {formatted_value}\n\n"
                            f"Current price {coin.symbol}: {formatted_price} USD"
                        )
                        triggered.append(message)
                        self.triggered_alerts.add(alert_key)

                else:
                    # сброс состояния если условие перестало выполняться
                    if alert_key in self.triggered_alerts:
                        self.triggered_alerts.remove(alert_key)

        # сохраняем состояние
        self._save_state()

        return triggered

    def _get_icon(self, symbol):
        icons = {
            "BTC": "₿",
            "ETH": "Ξ",
            "LTC": "Ł",
            "TIA": "🔹"
        }
        return icons.get(symbol, "💰")
