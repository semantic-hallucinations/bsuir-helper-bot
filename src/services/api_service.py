import httpx
from environs import Env

from config import setup_services_logging

env = Env()
env.read_env()

logger = setup_services_logging()


class ApiService:
    RAG_AGENT_API_URL = env.str("RAG_AGENT_API_URL")

    @classmethod
    async def get_response(cls, query: str) -> str:
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                async with client.stream(
                    "POST", cls.RAG_AGENT_API_URL, json={"message": query}
                ) as response:
                    response.raise_for_status()

                    full_text = ""
                    async for chunk in response.aiter_text():
                        full_text += chunk
                    return full_text
        except httpx.HTTPStatusError as e:
            logger.error(f"API error: {e.response.status_code} - {e.response.text}")
            raise RuntimeError(
                f"API error: {e.response.status_code} - {e.response.text}"
            ) from e
        except httpx.RequestError as e:
            logger.error("Error while connecting to RAG-service")
            raise RuntimeError("Error while connecting to RAG-service") from e
