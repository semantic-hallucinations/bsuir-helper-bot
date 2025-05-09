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
