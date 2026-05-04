import asyncio
from app.api.client import CoinGeckoClient
from app.config import load_config


async def main():
    config = load_config()

    client = CoinGeckoClient(
        base_url=config.api.base_url,
        timeout=config.api.timeout,
        max_retries=config.api.max_retries
    )

    await client.start()

    try:
        # 🔥 берём монеты из config
        coins = [coin.id for coin in config.coins]

        prices = await client.get_prices(coins)
        print(prices)

    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())