import json
import re

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
                formatted_response = ApiService.__format_response(response.json())
                return formatted_response
        except httpx.HTTPStatusError as e:
            logger.error(f"API error: {e.response.status_code} - {e.response.text}")
            raise RuntimeError(
                f"API error: {e.response.status_code} - {e.response.text}"
            ) from e
        except httpx.RequestError as e:
            logger.error("Error while connecting to RAG-service")
            raise RuntimeError("Error while connecting to RAG-service") from e

    @classmethod
    def __format_response(cls, response) -> str:
        response_text: str = response.get("response", "")
        response_text = re.sub(r"(?m)^#{1,6}\s*", "", response_text)

        sources = response.get("source_urls") or []

        if sources:
            sources_block = "\n\nИсточники:\n" + "\n".join(sources)
        else:
            sources_block = ""

        return response_text + sources_block
