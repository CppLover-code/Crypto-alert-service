from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

from app.worker import notify_users


def make_config():
    return SimpleNamespace(
        telegram=SimpleNamespace(enabled=True),
        email=SimpleNamespace(enabled=True),
    )


def make_user(**overrides):
    user = {
        "id": 2,
        "email": "anna@example.com",
        "telegram_chat_id": "123",
        "notify_email": True,
        "notify_telegram": True,
    }
    user.update(overrides)
    return user


async def test_does_not_send_telegram_when_flag_off():
    telegram = MagicMock()
    telegram.send_message = AsyncMock()
    email = MagicMock()
    email.send_email = AsyncMock()
    logger = MagicMock()

    user = make_user(notify_telegram=False, notify_email=False)

    await notify_users(
        ["alert"],
        [user],
        make_config(),
        telegram,
        email,
        logger,
    )

    telegram.send_message.assert_not_called()
    email.send_email.assert_not_called()


async def test_sends_telegram_when_flag_on():
    telegram = MagicMock()
    telegram.send_message = AsyncMock()
    email = MagicMock()
    email.send_email = AsyncMock()
    logger = MagicMock()

    user = make_user(notify_email=False, notify_telegram=True)

    await notify_users(
        ["alert"],
        [user],
        make_config(),
        telegram,
        email,
        logger,
    )

    telegram.send_message.assert_awaited()
    email.send_email.assert_not_called()


async def test_email_still_sent_if_telegram_fails():
    telegram = MagicMock()
    telegram.send_message = AsyncMock(side_effect=RuntimeError("telegram down"))
    email = MagicMock()
    email.send_email = AsyncMock()
    logger = MagicMock()

    await notify_users(
        ["alert"],
        [make_user()],
        make_config(),
        telegram,
        email,
        logger,
    )

    email.send_email.assert_awaited()