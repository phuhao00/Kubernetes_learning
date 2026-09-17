# AI 智能客服 Demo

> **个人实践项目** · 模拟企业交付流程 · 一人扮演 PO/PM/开发

可运行的 AI 客服演示：左侧用户对话，右侧知识库管理。支持 FAQ 导入/CRUD、关键词+相似度检索、未命中转人工，可选 LLM 润色。

## 快速启动

```bash
cd ai-cs-demo
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

浏览器打开：**http://localhost:8000**

### 可选：启用 LLM 润色

```bash
export OPENAI_API_KEY=sk-xxx          # 或 LLM_API_KEY
export OPENAI_BASE_URL=https://api.openai.com/v1   # 兼容 OpenAI 的网关
export LLM_MODEL=gpt-4o-mini
```

未配置 API Key 时，系统自动使用**检索直答**，Demo 仍可完整演示。

## 三场景演示脚本

| 场景 | 操作 | 预期结果 |
|------|------|----------|
| **1. 命中 FAQ** | 输入「怎么重置密码」 | 返回密码重置指引，标注「知识库命中」 |
| **2. 未命中→转人工** | 输入「你们有火星分店吗」 | 显示转人工提示，右侧「待人工处理」新增记录 |
| **3. 导入后提问** | 上传 `data/sample_faq.csv`，再问「发票怎么开」 | 返回开票说明（新导入的知识） |

### curl 快速验证

```bash
# 健康检查
curl http://localhost:8000/api/health

# 场景1：命中 FAQ
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"怎么重置密码"}'

# 场景2：转人工
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"你们有火星分店吗"}'

# 场景3：导入 CSV 后提问
curl -X POST http://localhost:8000/api/admin/faq/import-csv \
  -F "file=@data/sample_faq.csv"
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"发票怎么开"}'
```

## 项目结构

```
ai-cs-demo/
├── app/              # FastAPI 后端
├── static/           # 单页前端
├── data/             # SQLite 数据库 + 示例 CSV
├── pm/               # PM 交付物（中文）
└── requirements.txt
```

## PM 交付物

详见 [`pm/`](pm/) 目录：M1 范围、WBS、甘特图、RAID、变更日志、Dashboard、周报、验收清单、复盘与面试话术。

## 技术说明

- **后端**：FastAPI + SQLite
- **检索**：Jaccard 相似度 + 关键词匹配（无向量库，降低部署复杂度）
- **LLM**：可选，失败或未配置时回退检索原文
- **刻意不做**：登录鉴权、多租户、真实坐席桌面、生产级部署
