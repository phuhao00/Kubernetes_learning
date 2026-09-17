# 甘特图 · 模拟 3 周排期

> **标注**：以下为个人实践的模拟日历，非真实团队排期。

```mermaid
gantt
    title AI 客服 Demo · 个人实践甘特图（模拟 3 周）
    dateFormat  YYYY-MM-DD
    axisFormat  %m/%d

    section M1 需求范围确认
    需求访谈与范围文档           :m1a, 2026-09-01, 2d
    RAID初稿与WBS               :m1b, after m1a, 1d
    M1 里程碑评审               :milestone, m1, 2026-09-05, 0d

    section M2 方案/原型确认
    页面线框与API设计            :m2a, 2026-09-08, 2d
    数据模型与检索方案           :m2b, after m2a, 1d
    M2 里程碑评审               :milestone, m2, 2026-09-12, 0d

    section M3 Demo核心功能
    后端骨架与数据库             :m3a, 2026-09-15, 2d
    FAQ管理与导入               :m3b, after m3a, 2d
    检索与聊天转人工              :m3c, after m3b, 2d
    LLM可选集成                 :m3d, after m3c, 1d
    M3 里程碑评审               :milestone, m3, 2026-09-22, 0d

    section M4 Demo验收
    三场景测试与修Bug            :m4a, 2026-09-23, 2d
    验收清单签字                 :m4b, after m4a, 1d
    M4 里程碑评审               :milestone, m4, 2026-09-26, 0d

    section M5 交付与复盘
    PM文档补齐与Dashboard        :m5a, 2026-09-29, 2d
    复盘与面试材料                 :m5b, after m5a, 1d
    Git PR与作品集发布             :m5c, after m5b, 1d
    M5 项目关闭                 :milestone, m5, 2026-10-03, 0d
```

## 里程碑说明

| 里程碑 | 日期（模拟） | 完成标志 |
|--------|-------------|----------|
| **M1** 需求范围确认 | 09-05 | m1-scope.md 签字，6 条 US 冻结 |
| **M2** 方案/原型确认 | 09-12 | 左聊右管布局 + API 清单确认 |
| **M3** Demo核心完成 | 09-22 | 三场景代码可跑，种子 FAQ 可检索 |
| **M4** Demo验收完成 | 09-26 | 验收清单 3/3 通过 |
| **M5** 交付与复盘 | 10-03 | PR 合并，复盘 + 面试话术就绪 |
