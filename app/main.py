import asyncio

from app.api.client import CoinGeckoClient
from app.config import load_config
from app.services.price_service import PriceService
from app.services.alert_service import AlertService
from app.services.notifier import TelegramNotifier, EmailNotifier
from app.storage.file_storage import FileStorage
from app.utils.logger import setup_logger

async def main():
    config = load_config()

    logger = setup_logger(
        log_file=config.logging.file_path,
        level=config.logging.level
    )

    client = CoinGeckoClient(
        base_url=config.api.base_url,
        timeout=config.api.timeout,
        max_retries=config.api.max_retries
    )

    service = PriceService(client, config)
    alert_service = AlertService(config)

    storage = FileStorage(config.storage.file_path)

    telegram = TelegramNotifier(
        token=config.telegram.bot_token,
        chat_id=config.telegram.chat_id
    )

    email_notifier = EmailNotifier(config.email)

    await client.start()

    logger.info("Crypto Alert Service started")

    current_interval = config.interval_seconds
    max_interval = 300 # максимум 5 минут

    try:
        while True:
            try:
                logger.info("Fetching prices...")

                data = await service.fetch_prices()

                logger.info(f"Prices fetched: {data['prices']}")

                # возвращаем нормальный interval после успешного запроса
                current_interval = config.interval_seconds

                storage.save(data)

                alerts = alert_service.check_alerts(data['prices'])

                if alerts:
                    for alert in alerts:
                        logger.warning(alert)

                        #Telegram
                        if config.telegram.enabled:
                            await telegram.send_message(alert)

                        #Email
                        if config.email.enabled:
                            email_notifier.send_email(
                                subject="🚨 Crypto Alert",
                                body=alert
                            )
                
                logger.info(
                    f"Sleeping for {config.interval_seconds} seconds..."
                )
                await asyncio.sleep(current_interval)
            
            except Exception as e:
                logger.error(f"Loop error: {e}")

                # adaptive polling для rate limit
                if "429" in str(e):
                    current_interval = min(current_interval * 2, max_interval)

                    logger.warning(
                        f"Rate limit hit. Increasing interval to {current_interval} seconds"
                    )

                await asyncio.sleep(current_interval)

    except KeyboardInterrupt:
            logger.info("Service stopped by user")

    finally:
            await client.close()
            logger.info("HTTP client closed")


if __name__ == "__main__":
    asyncio.run(main())