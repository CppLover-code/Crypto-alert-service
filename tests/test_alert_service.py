from decimal import Decimal
from types import SimpleNamespace

from app.services.alert_service import AlertService

def make_config(tmp_path, alert_type="above", value=80000):
    return SimpleNamespace(
        coins=[
            SimpleNamespace(
                id="bitcoin",
                symbol="BTC",
                alerts=[{"type": alert_type, "value": value}],
            )
        ],
        alerts=SimpleNamespace(state_file=str(tmp_path / "state.json")),
    )
    
def test_fires_once_when_price_above(tmp_path):
    service = AlertService(make_config(tmp_path, "above", 80000))
    prices = {"bitcoin": Decimal("80000")}
    
    first = service.check_alerts(prices)
    second = service.check_alerts(prices)
    
    assert len(first) == 1
    assert "ABOVE" in first[0]
    assert second == []
    
def test_resets_when_price_goes_back(tmp_path):
    service = AlertService(make_config(tmp_path, "above", 80000))
    
    service.check_alerts({"bitcoin": Decimal("81000")})
    service.check_alerts({"bitcoin": Decimal("79000")})
    again = service.check_alerts({"bitcoin": Decimal("81000")})
    
    assert len(again) == 1
    
def test_below_alert(tmp_path):
    service = AlertService(make_config(tmp_path, "below", 80000))
    messages = service.check_alerts({"bitcoin": Decimal("49000")})
    
    assert len(messages) == 1
    assert "BELOW" in messages[0]