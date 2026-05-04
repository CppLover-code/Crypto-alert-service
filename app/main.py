import asyncio
from app.api.client import CoinGeckoClient

async def main():
    client = CoinGeckoClient(
        base_url= "https://api.coingecko.com/api/v3"
    )

    await client.start()

    try:
        prices = await client.get_prices(["bitcoin", "ethereum"])
        print(prices)

    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())