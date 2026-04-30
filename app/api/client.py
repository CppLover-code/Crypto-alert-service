import aiohttp
import asyncio
from typing import List, Dict


class CoinGeckoClient:
    def __init__(self, base_url: str, timeout: int = 5):
        self.base_url = base_url
        self.timeout = timeout

    async def get_prices(self, coins: List[str]) -> Dict[str, float]:
        if not coins:
            return {}

        url = f"{self.base_url}/simple/price"

        params = {
            "ids": ",".join(coins),
            "vs_currencies": "usd"
        }

        timeout = aiohttp.ClientTimeout(total=self.timeout)

        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url, params=params) as response:
                    
                    if response.status != 200:
                        raise RuntimeError(f"API error: {response.status}")

                    data = await response.json()

                    result = {}

                    for coin in coins:
                        if coin in data and "usd" in data[coin]:
                            result[coin] = data[coin]["usd"]
                        else:
                            result[coin] = None

                    return result

        except asyncio.TimeoutError:
            raise RuntimeError("API request timed out")

        except aiohttp.ClientError as e:
            raise RuntimeError(f"API request failed: {e}")