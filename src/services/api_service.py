import json

import httpx
from environs import Env

from config import setup_services_logging

env = Env()
env.read_env()

logger = setup_services_logging()


class ApiService:
    RAG_AGENT_API_URL = env.str("RAG_AGENT_API_URL")

    @classmethod
    async def get_response(cls, query: str) -> dict:
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    cls.RAG_AGENT_API_URL,
                    content=json.dumps(query),
                    headers={"Content-Type": "application/json"},
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"API error: {e.response.status_code} - {e.response.text}")
            raise RuntimeError(
                f"API error: {e.response.status_code} - {e.response.text}"
            ) from e
        except httpx.RequestError as e:
            logger.error("Error while connecting to RAG-service")
            raise RuntimeError("Error while connecting to RAG-service") from e
