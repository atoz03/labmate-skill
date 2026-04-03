# labmate.skill —— 产品需求文档 v1.0

---

## 一、产品概述

**labmate.skill** 是一个用于蒸馏“师兄 / 师姐 / 实验室前辈”的 meta-skill。

用户通过对话式交互提供：
- 论文 / technical report
- 实验记录 / 训练日志
- 组会纪要 / 答疑聊天
- 代码仓库 / PR / review 记录
- 以及主观描述

系统自动生成一个可独立运行的 **Mentor Persona + Research Skill**。

生成结果分成两个部分：
- **Part A — Research Skill**：研究方法、实验套路、写作与工程习惯
- **Part B — Mentor Persona**：答疑方式、带教风格、表达气质、边界与雷区

默认组合运行：**先像本人一样说话，再像本人一样指导。**

---

## 二、核心洞察

从“同事.skill”迁移到“labmate.skill”后，材料价值排序发生变化：

1. 论文、实验日志、组会纪要能更直接沉淀研究方法论
2. 人格的关键在于“怎么带人、怎么批评、怎么推进研究”
3. 能力的关键在于“问题拆解、实验设计、论文表达”

因此，本产品以**学术材料蒸馏**为核心场景。

---

## 三、目标用户

典型用户：
- 师兄毕业后，仍想延续他的研究方法与答疑方式的在读学生
- 课题组内部希望沉淀方法论的人
- 想复用前人实验经验、代码规范、写作套路的研究者
- 想做一个“数字师兄 / 师姐”进行趣味化知识管理的人

---

## 四、用户流程

### Step 1：录入基础信息
1. 如何称呼这位 Labmate
2. 学术档案（学校 / 实验室 / 年级 / 身份 / 方向）
3. 带教画像（MBTI / 风格标签 / 主观印象）

### Step 2：导入原材料
- 论文 / 技术报告
- 实验记录 / 训练日志 / W&B 导出
- 组会纪要 / 答疑聊天 / 语音转写
- 代码仓库 / PR / Issue / Review 评论
- 用户直接粘贴内容

### Step 3：双线分析
- 线路 A：抽取 Research Skill
- 线路 B：抽取 Mentor Persona

### Step 4：生成预览
分别给出 `work.md` 与 `persona.md` 的摘要，让用户确认。

### Step 5：写入 Skill
输出到：

```
labmates/{slug}/
```

### Step 6：持续进化
- 追加新材料 → 增量合并
- 用户纠正“这不像他” → 写入 Correction 层
- 支持版本回滚

---

## 五、输出文件结构

```
labmates/{slug}/
├── SKILL.md
├── work.md
├── persona.md
├── work_skill.md
├── persona_skill.md
├── meta.json
├── versions/
└── knowledge/
    ├── papers/
    ├── experiments/
    ├── meetings/
    └── code/
```

---

## 六、meta.json 建议结构

```json
{
  "name": "青云",
  "slug": "qing-yun",
  "created_at": "2026-04-03T00:00:00Z",
  "updated_at": "2026-04-03T00:00:00Z",
  "version": "v1",
  "profile": {
    "school": "上海交通大学",
    "lab": "ACL Lab",
    "cohort": "2021级",
    "role": "博士生",
    "field": "NLP Agent",
    "mbti": "INTJ"
  }
}
```

---

## 七、灵感来源与致谢

本项目的直接灵感来源于 **同事.skill**。

它提供了“通过原材料蒸馏出一个可调用 persona + capability skill”的产品骨架；
而 labmate.skill 做的事情，是把这个骨架迁移到科研场景：
- 原材料聚焦到论文、实验记录、组会纪要与代码 review
- 人格重点从职场协作，迁移到科研带教与答疑风格
- 能力重点从工程接班，迁移到研究方法论复用
