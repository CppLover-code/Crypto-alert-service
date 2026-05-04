import asyncio
from app.api.client import CoinGeckoClient
from app.config import load_config
from app.storage.file_storage import FileStorage
from app.services.price_service import PriceService


async def main():
    config = load_config()

    client = CoinGeckoClient(
        base_url=config.api.base_url,
        timeout=config.api.timeout,
        max_retries=config.api.max_retries
    )

    service = PriceService(client, config)

    storage = FileStorage(config.storage.file_path)

    await client.start()

    try:
        data = await service.fetch_prices()

        storage.save(data)

        print(data)

    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())