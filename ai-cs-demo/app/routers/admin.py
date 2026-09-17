import csv
import io
from datetime import datetime

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.database import get_connection
from app.models import FAQCreate, FAQImportRequest, FAQOut, FAQUpdate

router = APIRouter(prefix="/api/admin", tags=["admin"])


def row_to_faq(row) -> FAQOut:
    data = dict(row)
    data["enabled"] = bool(data["enabled"])
    return FAQOut(**data)


@router.get("/faq", response_model=list[FAQOut])
def list_faq():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM faq_entries ORDER BY id ASC"
        ).fetchall()
    return [row_to_faq(r) for r in rows]


@router.post("/faq", response_model=FAQOut)
def create_faq(body: FAQCreate):
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO faq_entries (question, answer, keywords, enabled) VALUES (?, ?, ?, ?)",
            (body.question, body.answer, body.keywords, int(body.enabled)),
        )
        conn.commit()
        row = conn.execute(
            "SELECT * FROM faq_entries WHERE id = ?", (cur.lastrowid,)
        ).fetchone()
    return row_to_faq(row)


@router.put("/faq/{faq_id}", response_model=FAQOut)
def update_faq(faq_id: int, body: FAQUpdate):
    with get_connection() as conn:
        existing = conn.execute(
            "SELECT * FROM faq_entries WHERE id = ?", (faq_id,)
        ).fetchone()
        if not existing:
            raise HTTPException(404, "FAQ 不存在")

        question = body.question if body.question is not None else existing["question"]
        answer = body.answer if body.answer is not None else existing["answer"]
        keywords = body.keywords if body.keywords is not None else existing["keywords"]
        enabled = (
            int(body.enabled)
            if body.enabled is not None
            else existing["enabled"]
        )
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        conn.execute(
            "UPDATE faq_entries SET question=?, answer=?, keywords=?, enabled=?, updated_at=? WHERE id=?",
            (question, answer, keywords, enabled, now, faq_id),
        )
        conn.commit()
        row = conn.execute(
            "SELECT * FROM faq_entries WHERE id = ?", (faq_id,)
        ).fetchone()
    return row_to_faq(row)


@router.delete("/faq/{faq_id}")
def delete_faq(faq_id: int):
    with get_connection() as conn:
        cur = conn.execute("DELETE FROM faq_entries WHERE id = ?", (faq_id,))
        conn.commit()
        if cur.rowcount == 0:
            raise HTTPException(404, "FAQ 不存在")
    return {"ok": True}


@router.post("/faq/import-csv")
async def import_csv(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8-sig")
    return _import_csv_text(text)


@router.post("/faq/import-text")
def import_text(body: FAQImportRequest):
    return _import_csv_text(body.text)


def _import_csv_text(text: str) -> dict:
    reader = csv.DictReader(io.StringIO(text))
    required = {"question", "answer"}
    if not reader.fieldnames or not required.issubset(set(reader.fieldnames)):
        raise HTTPException(400, "CSV 需包含 question, answer 列（可选 keywords）")

    imported = 0
    with get_connection() as conn:
        for row in reader:
            q = (row.get("question") or "").strip()
            a = (row.get("answer") or "").strip()
            kw = (row.get("keywords") or "").strip()
            if not q or not a:
                continue
            conn.execute(
                "INSERT INTO faq_entries (question, answer, keywords, enabled) VALUES (?, ?, ?, 1)",
                (q, a, kw),
            )
            imported += 1
        conn.commit()
    return {"imported": imported}
