from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Coin, Price, User


def add_coin(session: Session, coingecko_id: str, symbol: str) -> Coin:
    coin = Coin(coingecko_id=coingecko_id, symbol=symbol, enabled=True)
    session.add(coin)
    session.flush()
    return coin


def upsert_price(session: Session, coin_id: int, value: Decimal) -> Price:
    price = session.scalar(select(Price).where(Price.coin_id == coin_id))
    now = datetime.now(timezone.utc).replace(tzinfo=None)

    if price is None:
        price = Price(coin_id=coin_id, value=value, updated_at=now)
        session.add(price)
    else:
        price.value = value
        price.updated_at = now

    return price


def get_price_for_coin(session: Session, coin_id: int) -> Price | None:
    return session.scalar(select(Price).where(Price.coin_id == coin_id))


def add_user(
    session: Session,
    name: str,
    email: str | None = None,
    telegram_chat_id: str | None = None,
    notify_email: bool = False,
    notify_telegram: bool = False,
) -> User:
    user = User(
        name=name,
        email=email,
        telegram_chat_id=telegram_chat_id,
        notify_email=notify_email,
        notify_telegram=notify_telegram,
        active=True,
    )
    session.add(user)
    session.flush()
    return user