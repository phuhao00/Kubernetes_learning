from fastapi import APIRouter

from app.database import get_connection
from app.kb_service import search_faq
from app.llm_service import polish_answer
from app.models import ChatRequest, ChatResponse, HumanConversationOut

router = APIRouter(prefix="/api/chat", tags=["chat"])

ESCALATION_MSG = (
    "抱歉，我暂时无法回答这个问题。已为您转接人工客服，请稍候。"
    "（演示模式：您的提问已记录到待处理列表）"
)


@router.post("", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    message = req.message.strip()
    match = search_faq(message)

    with get_connection() as conn:
        if match:
            reply = match["answer"]
            source = "retrieval"
            polished = await polish_answer(message, match["answer"])
            if polished:
                reply = polished
                source = "llm"

            conn.execute(
                "INSERT INTO chat_messages (role, content, matched_faq_id, escalated) VALUES (?, ?, ?, 0)",
                ("user", message, None),
            )
            conn.execute(
                "INSERT INTO chat_messages (role, content, matched_faq_id, escalated) VALUES (?, ?, ?, 0)",
                ("assistant", reply, match["id"]),
            )
            conn.commit()

            return ChatResponse(
                reply=reply,
                matched=True,
                matched_faq_id=match["id"],
                escalated=False,
                source=source,
            )

        conn.execute(
            "INSERT INTO chat_messages (role, content, matched_faq_id, escalated) VALUES (?, ?, NULL, 1)",
            ("user", message),
        )
        conn.execute(
            "INSERT INTO chat_messages (role, content, matched_faq_id, escalated) VALUES (?, ?, NULL, 1)",
            ("assistant", ESCALATION_MSG),
        )
        conn.execute(
            "INSERT INTO human_conversations (user_message, status) VALUES (?, 'pending')",
            (message,),
        )
        conn.commit()

    return ChatResponse(
        reply=ESCALATION_MSG,
        matched=False,
        escalated=True,
        source="escalation",
    )


@router.get("/history")
def chat_history(limit: int = 50):
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, role, content, matched_faq_id, escalated, created_at "
            "FROM chat_messages ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [dict(r) for r in reversed(rows)]


@router.get("/human-queue", response_model=list[HumanConversationOut])
def human_queue():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, user_message, status, created_at FROM human_conversations "
            "WHERE status = 'pending' ORDER BY id DESC"
        ).fetchall()
    return [HumanConversationOut(**dict(r)) for r in rows]
