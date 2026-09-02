import asyncio

from app.api.client import CoinGeckoClient
from app.config import load_config
from app.db import get_session, init_db
from app.services.price_service import PriceService
from app.services.alert_service import AlertService
from app.services.notifier import TelegramNotifier, EmailNotifier
from app.storage.file_storage import FileStorage
from app.storage.repositories import ensure_coins, save_api_prices
from app.utils.logger import setup_logger


async def run_worker() -> None:
    config = load_config()
    logger = setup_logger(
        log_file=config.logging.file_path,
        level=config.logging.level,
    )

    init_db()
    session = get_session()
    try:
        ensure_coins(session, config.coins)
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

    client = CoinGeckoClient(
        base_url=config.api.base_url,
        timeout=config.api.timeout,
        max_retries=config.api.max_retries,
    )
    await client.start()

    service = PriceService(client, config)
    alert_service = AlertService(config)
    storage = FileStorage(config.storage.file_path)

    telegram = TelegramNotifier(
        token=config.telegram.bot_token,
        chat_id=config.telegram.chat_id,
    )
    await telegram.start()
    email_notifier = EmailNotifier(config.email)

    logger.info("Crypto Alert Service started")

    current_interval = config.interval_seconds
    max_interval = 300

    try:
        while True:
            try:
                logger.info("Fetching prices...")
                data = await service.fetch_prices()
                logger.info(f"Prices fetched: {data['prices']}")
                current_interval = config.interval_seconds

                storage.save(data)

                db_session = get_session()
                try:
                    save_api_prices(db_session, data["prices"])
                    db_session.commit()
                except Exception:
                    db_session.rollback()
                    raise
                finally:
                    db_session.close()

                alerts = alert_service.check_alerts(data["prices"])
                if alerts:
                    for alert in alerts:
                        logger.warning(alert)
                        if config.telegram.enabled:
                            await telegram.send_message(alert)
                        if config.email.enabled:
                            await email_notifier.send_email(
                                subject="🚨 Crypto Alert",
                                body=alert,
                            )

                logger.info(f"Sleeping for {current_interval} seconds...")
                await asyncio.sleep(current_interval)

            except Exception as e:
                logger.error(f"Loop error: {e}")
                if "429" in str(e):
                    current_interval = min(current_interval * 2, max_interval)
                    logger.warning(
                        f"Rate limit hit. Increasing interval to {current_interval} seconds"
                    )
                await asyncio.sleep(current_interval)

    except asyncio.CancelledError:
        logger.info("Application shutdown requested")
        raise
    finally:
        await client.close()
        await telegram.close()
        logger.info("Application stopped")