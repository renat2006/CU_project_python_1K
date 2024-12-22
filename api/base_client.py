import aiohttp
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseClient:
    def __init__(self, base_url, timeout=30):
        self.base_url = base_url
        self.timeout = timeout

    async def _request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}/{endpoint}"
        logger.info(f"Отправка {method}-запроса на {url} с параметрами: {kwargs}")
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, timeout=self.timeout, **kwargs) as response:
                if response.status != 200:
                    logger.error(f"Ошибка API: {response.status} - {await response.text()}")
                    raise Exception(f"Ошибка API: {response.status} - {await response.text()}")
                return await response.json()

    async def get(self, endpoint, params=None, headers=None):
        return await self._request("GET", endpoint, params=params, headers=headers)