# WBS · 工作分解结构

> 映射里程碑 M1–M5 · 个人实践 · 模拟 3 周排期

| WBS ID | 工作包 | 负责人 | 里程碑 | 工期 | 交付物 |
|--------|--------|--------|--------|------|--------|
| 1.0 | **项目管理** | PM（本人） | M1–M5 | 3 周 | pm/ 全套文档 |
| 1.1 | 需求访谈 & 范围定义 | PM | M1 | 1d | m1-scope.md |
| 1.2 | RAID 初稿 & 排期 | PM | M1 | 0.5d | raid.md, gantt.md |
| 1.3 | 周报 & Dashboard | PM | M4–M5 | 持续 | weekly-report-*.md, dashboard.html |
| 1.4 | 验收 & 复盘 | PM | M5 | 1d | acceptance-checklist.md, retrospective.md |
| 2.0 | **方案设计** | PM + Dev | M2 | 3d | 线框意图、API 草图 |
| 2.1 | 页面布局（左聊右管） | PM | M2 | 0.5d | 手绘线框 → static/ |
| 2.2 | API 设计（chat/admin） | Dev | M2 | 1d | routers/ |
| 2.3 | 数据模型 & 检索策略 | Dev | M2 | 1d | database.py, kb_service.py |
| 2.4 | 技术选型确认 | PM | M2 | 0.5d | README 技术说明 |
| 3.0 | **Demo 开发** | Dev | M3 | 5d | 可运行应用 |
| 3.1 | FastAPI 骨架 & SQLite | Dev | M3 | 1d | app/main.py |
| 3.2 | FAQ CRUD + 导入 | Dev | M3 | 1.5d | admin.py, 前端管理区 |
| 3.3 | 检索引擎 | Dev | M3 | 1d | kb_service.py |
| 3.4 | 聊天 & 转人工 | Dev | M3 | 1d | chat.py |
| 3.5 | 前端联调 & 样式 | Dev | M3 | 0.5d | static/ |
| 3.6 | 可选 LLM 集成 | Dev | M3 | 0.5d | llm_service.py |
| 4.0 | **测试 & 验收** | PM + Dev | M4 | 2d | 三场景通过 |
| 4.1 | curl / 手动三场景 | Dev | M4 | 0.5d | README 脚本 |
| 4.2 | 验收清单执行 | PM | M4 | 0.5d | acceptance-checklist.md |
| 4.3 | Bug 修复（阈值调优） | Dev | M4 | 1d | kb_service 参数 |
| 5.0 | **交付 & 复盘** | PM | M5 | 2d | PR + 作品集 |
| 5.1 | README & 演示脚本 | PM | M5 | 0.5d | README.md |
| 5.2 | 面试话术 & 简历一行 | PM | M5 | 0.5d | interview-talk-track.md |
| 5.3 | 项目复盘 | PM | M5 | 0.5d | retrospective.md |
| 5.4 | Git 提交 & PR | Dev | M5 | 0.5d | feature branch |

## WBS → 里程碑映射

```
M1 需求范围确认    ← 1.1, 1.2
M2 方案/原型确认   ← 2.1–2.4
M3 Demo核心完成    ← 3.1–3.6
M4 Demo验收完成    ← 4.1–4.3
M5 交付与复盘      ← 5.1–5.4, 1.3, 1.4
```
