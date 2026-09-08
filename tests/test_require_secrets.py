from types import SimpleNamespace

import pytest

from app.config import require_secrets


def test_ok_when_channels_disabled():
    config = SimpleNamespace(
        telegram=SimpleNamespace(enabled=False, bot_token=None),
        email=SimpleNamespace(
            enabled=False,
            sender_email=None,
            app_password=None,
        ),
    )
    require_secrets(config)


def test_fails_without_telegram_token():
    config = SimpleNamespace(
        telegram=SimpleNamespace(enabled=True, bot_token=None),
        email=SimpleNamespace(
            enabled=False,
            sender_email=None,
            app_password=None,
        ),
    )
    with pytest.raises(RuntimeError, match="TELEGRAM_TOKEN"):
        require_secrets(config)