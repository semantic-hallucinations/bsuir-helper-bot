import asyncio
import json

import httpx
from environs import Env

from config import get_logger

from .message_formatter import format_rag_agent_response

env = Env()
env.read_env()

logger = get_logger("bot.services")


class ApiService:
    RAG_AGENT_API_URL = env.str("RAG_AGENT_API_URL")
    MAX_RETRIES = 3

    @classmethod
    async def get_response(cls, query: str) -> dict:
        for attempt in range(cls.MAX_RETRIES):
            try:
                async with httpx.AsyncClient(timeout=60.0) as client:
                    response = await client.post(
                        cls.RAG_AGENT_API_URL,
                        content=json.dumps(query),
                        headers={"Content-Type": "application/json"},
                    )
                    response.raise_for_status()
                    return format_rag_agent_response(response.json())
            except (httpx.RequestError, httpx.HTTPStatusError) as e:
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt == cls.MAX_RETRIES - 1:
                    logger.error("All retry attempts failed")
                    raise RuntimeError("Failed to get response from RAG-service") from e
                await asyncio.sleep(2**attempt)
