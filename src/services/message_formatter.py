import re


def format_rag_agent_response(response) -> str:
    response_text: str = response.get("response", "")
    response_text = re.sub(r"(?m)^#{1,6}\s*", "", response_text)
    response_text = "**" + response_text + "**"

    sources = response.get("source_urls") or []
    sources = list(set(sources))

    if sources:
        sources_block = "\n\nИсточники:\n" + "\n".join(sources)
    else:
        sources_block = ""

    return response_text + sources_block


def strip_markdown(text: str) -> str:
    # Заголовки (удалить #)
    text = re.sub(r"(?m)^\s{0,3}#+\s*", "", text)

    # Блоки кода ```
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)

    # Однострочный код `
    text = re.sub(r"`+", "", text)

    # Картинки: ![alt](url) → alt (url)
    text = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)", r"\1 (\2)", text)
    text = re.sub(r"!\[([^\]]*)\]\(([^)\n]+)", r"\1 (\2)", text)

    # Правильные ссылки: [текст](url) → текст (url)
    text = re.sub(r"\[([^\]]+)\]\((https?://[^\s\)]+)\)", r"\1 (\2)", text)

    # Незакрытая ссылка: [текст](url → текст (url)
    text = re.sub(r"\[([^\]]+)\]\((https?://[^\s\)]+)", r"\1 (\2)", text)

    # Незакрытый текст ссылки: [пример ссылки(https://...) → пример ссылки (https://...)
    text = re.sub(r"\[([^\[\]()\n]+)\((https?:\/\/[^\s\)]+)\)", r"\1 (\2)", text)

    # Добавить закрывающую скобку, если не хватает
    text = re.sub(r"(?<!\))\((https?://[^\s\)]+)(?!\))(?=\s|$)", r"(\1)", text)

    # Удалить лишние закрывающие скобки после URL: (https://...)) → (https://...)
    text = re.sub(r"\((https?://[^\s\)]+)\)\)+", r"(\1)", text)

    # Удалить * _ ~
    text = re.sub(r"(\*\*|__|~~|[*_~])", "", text)

    return text.strip()


def preclean_for_md2(text: str) -> str:
    # Экранируем только . и !
    return text.replace(".", r"\.").replace("!", r"\!")
