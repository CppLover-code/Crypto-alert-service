from decimal import Decimal

from app.db import get_session, init_db
from app.storage.repositories import add_coin, add_user, get_price_for_coin, upsert_price


def main() -> None:
    init_db()
    session = get_session()

    try:
        coin = add_coin(session, "bitcoin", "BTC")
        upsert_price(session, coin.id, Decimal("80000.50"))
        user = add_user(
            session,
            name="Maria",
            email="maria@example.com",
            notify_email=True,
            notify_telegram=False,
        )
        session.commit()

        price = get_price_for_coin(session, coin.id)
        print("User:", user.id, user.name, user.email, user.notify_email)
        print("Coin:", coin.id, coin.symbol)
        print("Price:", price.value, "at", price.updated_at)
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()