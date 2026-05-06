import aiohttp
import asyncio
from typing import List, Dict, Optional
from decimal import Decimal


class CoinGeckoClient:
    def __init__(
        self,
        base_url: str,
        timeout: int = 5,
        max_retries: int = 3
    ):
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.session: Optional[aiohttp.ClientSession] = None

    async def start(self):
        """Инициализация HTTP-сессии"""
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        self.session = aiohttp.ClientSession(timeout=timeout)

    async def close(self):
        """Закрытие HTTP-сессии"""
        if self.session:
            await self.session.close()

    async def get_prices(self, coins: List[str]) -> Dict[str, float]:
        if not coins:
            return {}

        if not self.session:
            raise RuntimeError("Client session is not initialized. Call start().")

        url = f"{self.base_url}/simple/price"

        params = {
            "ids": ",".join(coins),
            "vs_currencies": "usd",
            "precision": "full"
        }

        for attempt in range(1, self.max_retries + 1):
            try:
                async with self.session.get(url, params=params) as response:

                    if response.status != 200:
                        raise RuntimeError(f"API error: {response.status}")

                    data = await response.json()

                    result = {}

                    for coin in coins:
                        if coin in data and "usd" in data[coin]:
                            result[coin] = Decimal(str(data[coin]["usd"]))
                        else:
                            result[coin] = None

                    return result

            except asyncio.TimeoutError:
                if attempt == self.max_retries:
                    raise RuntimeError("API request timed out")
                await asyncio.sleep(1)

            except aiohttp.ClientError as e:
                if attempt == self.max_retries:
                    raise RuntimeError(f"API request failed: {e}")
                await asyncio.sleep(1)