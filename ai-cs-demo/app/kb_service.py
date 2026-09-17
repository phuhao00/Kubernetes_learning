import re
from typing import Optional

from app.database import get_connection

STOP_WORDS = {"的", "了", "吗", "呢", "是", "在", "我", "有", "怎么", "如何", "什么", "哪", "能", "可以"}


def tokenize(text: str) -> set[str]:
    text = text.lower().strip()
    tokens = set(re.findall(r"[\u4e00-\u9fff]+|[a-z0-9]+", text))
    return {t for t in tokens if t not in STOP_WORDS and len(t) > 0}


def jaccard_similarity(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    intersection = len(a & b)
    union = len(a | b)
    return intersection / union if union else 0.0


def keyword_score(query: str, question: str, keywords: str) -> float:
    q = query.lower()
    score = 0.0
    for kw in re.split(r"[,，\s]+", keywords):
        kw = kw.strip().lower()
        if kw and kw in q:
            score += 0.35
    if question.lower() in q or q in question.lower():
        score += 0.4
    return min(score, 1.0)


def search_faq(query: str, threshold: float = 0.18) -> Optional[dict]:
    query_tokens = tokenize(query)
    best: Optional[dict] = None
    best_score = 0.0

    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, question, answer, keywords FROM faq_entries WHERE enabled = 1"
        ).fetchall()

    for row in rows:
        question_tokens = tokenize(row["question"])
        answer_tokens = tokenize(row["answer"])
        kw_tokens = tokenize(row["keywords"].replace(",", " "))

        sim_q = jaccard_similarity(query_tokens, question_tokens)
        sim_a = jaccard_similarity(query_tokens, answer_tokens) * 0.5
        sim_kw = jaccard_similarity(query_tokens, kw_tokens) * 0.8
        kw_hit = keyword_score(query, row["question"], row["keywords"])

        total = max(sim_q, sim_a, sim_kw, kw_hit)
        if total > best_score:
            best_score = total
            best = dict(row)

    if best and best_score >= threshold:
        best["score"] = best_score
        return best
    return None
