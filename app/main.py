import asyncio
from app.api.client import CoinGeckoClient
from app.config import load_config
from app.storage.file_storage import FileStorage
from app.services.price_service import PriceService
from app.utils.logger import setup_logger
from app.services.alert_service import AlertService


async def main():
    config = load_config()
    alert_service = AlertService(config)

    # создаём логгер
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
    storage = FileStorage(config.storage.file_path)

    await client.start()

    try:
        
        logger.info("Fetching prices...")

        data = await service.fetch_prices()

        logger.info(f"Prices fetched: {data['prices']}")

        alerts = alert_service.check_alerts(data["prices"])

        if alerts:
            logger.warning(f"ALERT! Threshold exceeded: {alerts}")

        storage.save(data)

        logger.info("Data saved successfully")

    except Exception as e:
        logger.error(f"Error occurred: {e}")

    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())