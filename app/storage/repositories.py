from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

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

def list_coins_with_prices(session: Session) -> list[Coin]:
    stmt = (
        select(Coin)
        .where(Coin.enabled.is_(True))
        .options(selectinload(Coin.price))
        .order_by(Coin.symbol)
    )
    return list(session.scalars(stmt).all())

def get_coin_by_coingecko_id(session: Session, coingecko_id: str) -> Coin | None:
    return session.scalar(
        select(Coin).where(Coin.coingecko_id == coingecko_id)
    )


def ensure_coins(session: Session, coins_from_config) -> None:
    for item in coins_from_config:
        existing = get_coin_by_coingecko_id(session, item.id)
        if existing is None:
            add_coin(session, item.id, item.symbol)


def save_api_prices(session: Session, prices: dict) -> None:
    for coingecko_id, value in prices.items():
        if value is None:
            continue
        coin = get_coin_by_coingecko_id(session, coingecko_id)
        if coin is None:
            continue
        upsert_price(session, coin.id, value)

def list_users(session: Session) -> list[User]:
    stmt = select(User).order_by(User.id)
    return list(session.scalars(stmt).all())

def get_user(session: Session, user_id: int) -> User | None:
    return session.get(User, user_id)

def deactivate_user(session: Session, user_id: int) -> User | None:
    user = get_user(session, user_id)
    if user is None:
        return None
    user.active = False
    return user

