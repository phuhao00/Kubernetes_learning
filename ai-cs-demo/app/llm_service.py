import os
from typing import Optional

import httpx


async def polish_answer(question: str, raw_answer: str) -> Optional[str]:
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")
    if not api_key:
        return None

    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model = os.getenv("LLM_MODEL", "gpt-4o-mini")

    prompt = (
        "你是客服助手。根据用户问题和知识库原文，用简洁友好的中文回答。"
        "不要编造知识库没有的信息。保持 2-4 句话。\n\n"
        f"用户问题：{question}\n知识库原文：{raw_answer}"
    )

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(
                f"{base_url.rstrip('/')}/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                    "max_tokens": 300,
                },
            )
            resp.raise_for_status()
            data = resp.json()
            content = data["choices"][0]["message"]["content"].strip()
            return content if content else None
    except Exception:
        return None
