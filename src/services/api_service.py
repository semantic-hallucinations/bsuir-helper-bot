import asyncio
import random
import aiohttp
from environs import Env

env = Env()
env.read_env()

API_URL = env.str("API_URL")  

class ApiService:
    async def __get_cat_image_url(self) -> str:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(API_URL) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data[0]["url"] 
                    else:
                        return "https://http.cat/404"  
        except Exception as e:
            print(f"Ошибка при получении картинки: {e}")
            return "https://http.cat/500"  

    async def get_response(self, query: str):
        await asyncio.sleep(random.uniform(0.5, 2.0))  

        responses = [
            "Это тестовый ответ от RAG-системы.",
            "Ассистент сейчас занят, попробуйте повторить запрос позже",
        ]

        if random.random() < 0.3:  
            image_url = await self.__get_cat_image_url()
            return f"Ассистент недоступен сейчас. Посмотрите на картинку кота:\n{image_url}"
        else:
            return random.choice(responses)