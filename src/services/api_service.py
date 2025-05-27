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
    async def get_response(cls, query: str) -> str:
        for attempt in range(cls.MAX_RETRIES):
            try:
                async with httpx.AsyncClient(timeout=120.0) as client:
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
                await asyncio.sleep(2**attempt * 3)


#     @classmethod
#     async def get_response(cls, query:str) -> str:
#         broken_markdowns = [
#         "Это *важный текст, но без закрытия звёздочки",
#         "Неправильное _курсивное выделение без конца",
#         "Ссылка без конца [пример ссылки(https://example.com)",
#         "*Жирный текст **вложенный* но сломан",
#         "```код без закрытия",
#         "Вот `однострочный код с незакрытым символом",
#         "Попытка использовать __подчёркивание__ и _курсив",  # лишняя нижняя черта
#         "Список:\n- пункт 1\n- пункт *с ошибкой\n- пункт 3",
#         "Вот [ссылка](https://example.com без закрытия скобки",
#         "Вот пример ***жирного и курсивного**, но поломан",
#         "Невалидная ссылка: [текст](ht@tp://bad_url)",
#         "Картинка без закрытия ![alt текст](image.png",
#         "~~зачёркнуто, но без закрытия",
#         "Вложенный формат: *текст _внутри без конца*",
#         "Жирный с экранированием\\*звезда без закрытия",
#         "Много **открытий *и не хватает* парных",
#         "Обычный текст с лишним `одним бэктиком",
#         "Проблемный [линк](https://example.com) и *курсив",
#         "## Заголовок без пробела",
#         "- пункт с _курсивом\n- второй с **жирным",
#     ]
#         return (
#     "**В БГУИР *блинчики* можно найти в нескольких местах:**\n\n"
#     "**1. Столовые университета**\n"
#     "В меню столовых №1, №2 и №3 иногда бывают блинчики (обычно в утренние часы или как десерт).\n"
#     "🔹 **Ссылки на актуальные меню:**\n"
#     "- [Столовая №1](https://www.bsuir.by/m/12_100229_1_194548.xls)\n"
#     "- [Столовая №2](https://www.bsuir.by/m/12_100229_1_194547.xls)\n"
#     "- [Столовая №3](https://www.bsuir.by/m/12_100229_1_194546.xls)\n\n"
#     "**2. Буфеты и кофейни**\n"
#     "В корпусах и общежитиях есть буфеты и кофейни, где могут подавать блинчики "
#     "(например, в кофейне 4-го корпуса или буфете 5-го корпуса).\n\n"
#     "**3. Столовые общежитий**\n"
#     "В столовых при общежитиях (особенно в №3 и №5) иногда готовят блинчики.\n\n"
#     "**4. В дни акций и мероприятий**\n"
#     "Во время студенческих праздников или тематических дней в столовых могут предлагать "
#     "блинчики по спецпредложению.\n\n"
#     "**Совет:** Если в меню нет блинчиков, уточните у сотрудников, в какие дни их готовят.\n\n"
#     "Хотите узнать про конкретную столовую или корпус? Уточните – помогу найти ближайший вариант! 😊\n\n"
#     "Источники:\n"
#     "https://www.bsuir.by/ru/obosoblennoe-podrazdelenie-bguir-kombinat-pitaniya\n"
#     "https://www.bsuir.by/ru/spetsialnosti-bguir\n"
#     "https://www.bsuir.by/ru/brsm-bguir\n"
#     "https://www.bsuir.by/ru/molodezhnye-obedineniya/volonterskiy-tsentr-bguir\n"
#     "https://www.bsuir.by/ru/bguir-v-pechati-za-sentyabr-2019\n"
#     "https://www.bsuir.by/ru/sotsialnaya-podderzhka"
# )
