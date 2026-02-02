import random
import asyncio
import httpx
from typing import Optional
from infrastructure.logger import get_logger

logger = get_logger("APIClient")

class ChaosError(Exception):
    pass

class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=base_url, verify=False)

    async def close(self):
        await self.client.aclose()

    async def _request(self, method: str, endpoint: str, **kwargs) -> httpx.Response:
        # 🐛 BUG HUNTING ZONE 🐛 
        # Намеренные баги для обучения студента
        
        # Bug #1: Random Timeout (Flakiness)
        # Если в endpoint есть слово 'slow', с вероятностью 30% кидаем таймаут
        if "slow" in endpoint and random.random() < 0.3:
            logger.warning("CHAOS: Simulating Network Timeout...")
            await asyncio.sleep(2) # Fake lag
            raise httpx.ReadTimeout("Chaos Monkey struck again!")

        # Bug #2: Auth Header missing for admin routes
        # Если идем в admin, но нет хедера X-Auth-Token - ошибка (хотя в коде студента мб она и передана, мы её "теряем")
        if "/admin" in endpoint and random.random() < 0.1:
             logger.warning("CHAOS: Dropping Auth Header...")
             if 'headers' in kwargs:
                 kwargs['headers'].pop('X-Auth-Token', None)

        url = f"{self.base_url}{endpoint}"
        logger.info(f"REQUEST: {method} {url} | Params: {kwargs.get('params')} | JSON: {kwargs.get('json')}")
        
        try:
            response = await self.client.request(method, endpoint, **kwargs)
            
            # Bug #3: 500 Error for specific ID
            # Если вернулся User ID 666 - подменяем статус на 500
            if "666" in response.text:
                logger.warning("CHAOS: Evil ID detected. Returning 500.")
                # Monkey patch response status (hacky but works for sim)
                response.status_code = 500
                
            logger.info(f"RESPONSE: {response.status_code} | Body: {response.text[:200]}...")
            return response
        except Exception as e:
            logger.error(f"REQUEST FAILED: {e}")
            raise

    async def get(self, endpoint: str, params: Optional[dict] = None) -> httpx.Response:
        return await self._request("GET", endpoint, params=params)

    async def post(self, endpoint: str, json: Optional[dict] = None) -> httpx.Response:
        return await self._request("POST", endpoint, json=json)
        
    async def put(self, endpoint: str, json: Optional[dict] = None) -> httpx.Response:
        return await self._request("PUT", endpoint, json=json)
        
    async def delete(self, endpoint: str) -> httpx.Response:
        return await self._request("DELETE", endpoint)
