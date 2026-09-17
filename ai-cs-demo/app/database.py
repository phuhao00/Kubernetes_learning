import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "app.db"


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS faq_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                keywords TEXT DEFAULT '',
                enabled INTEGER DEFAULT 1,
                created_at TEXT DEFAULT (datetime('now')),
                updated_at TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                matched_faq_id INTEGER,
                escalated INTEGER DEFAULT 0,
                created_at TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS human_conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_message TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TEXT DEFAULT (datetime('now'))
            );
            """
        )
        count = conn.execute("SELECT COUNT(*) FROM faq_entries").fetchone()[0]
        if count == 0:
            seed_faqs(conn)


def seed_faqs(conn: sqlite3.Connection) -> None:
    samples = [
        (
            "如何重置密码？",
            "进入登录页点击「忘记密码」，输入注册邮箱即可收到重置链接。链接 30 分钟内有效。",
            "密码,重置,忘记密码,登录",
        ),
        (
            "支持哪些支付方式？",
            "目前支持微信支付、支付宝和银联卡。企业客户可申请对公转账。",
            "支付,付款,微信,支付宝,银联",
        ),
        (
            "订单多久能发货？",
            "现货订单 24 小时内发货，预售商品按商品页标注时间发货。",
            "发货,物流,配送,多久",
        ),
        (
            "如何申请退款？",
            "在「我的订单」中选择对应订单，点击「申请退款」并填写原因。未发货订单 1-3 个工作日原路退回。",
            "退款,退货,取消订单",
        ),
        (
            "会员有什么权益？",
            "会员享受全场 9 折、免运费、专属客服和生日礼券。年费 99 元。",
            "会员,VIP,权益,折扣",
        ),
    ]
    conn.executemany(
        "INSERT INTO faq_entries (question, answer, keywords) VALUES (?, ?, ?)",
        samples,
    )
