from typing import Optional

from pydantic import BaseModel, Field


class FAQCreate(BaseModel):
    question: str = Field(..., min_length=1)
    answer: str = Field(..., min_length=1)
    keywords: str = ""
    enabled: bool = True


class FAQUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None
    keywords: Optional[str] = None
    enabled: Optional[bool] = None


class FAQOut(BaseModel):
    id: int
    question: str
    answer: str
    keywords: str
    enabled: bool
    created_at: str
    updated_at: str


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)


class ChatResponse(BaseModel):
    reply: str
    matched: bool
    matched_faq_id: Optional[int] = None
    escalated: bool = False
    source: str = "retrieval"


class HumanConversationOut(BaseModel):
    id: int
    user_message: str
    status: str
    created_at: str


class FAQImportRequest(BaseModel):
    text: str = Field(..., min_length=1)
