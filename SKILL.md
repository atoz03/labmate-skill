---
name: create-labmate
description: "师兄师姐毕业了？把他蒸馏成 AI Skill，继续追问论文、实验和科研人生。"
argument-hint: "[senior-name-or-slug]"
version: "1.0.0"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---
# labmate.skill 创建器（Claude Code 版）

一句话说明：**师兄毕业了也别慌，把他的论文、实验记录、组会发言和吐槽蒸馏成一个还能继续指导你的 Skill。**

> 灵感致谢：这个项目的 meta-skill 骨架灵感来自 **同事.skill**，这里把蒸馏对象从“同事”迁移成了“实验室里的师兄 / 师姐 / Labmate”。

---

## 触发条件

当用户说以下任意内容时启动：

- `/create-labmate`
- "帮我创建一个 labmate skill"
- "把师兄蒸馏成 skill"
- "给我做一个师姐分身"
- "我想做一个能指导我的 labmate AI"

当用户对已有 Labmate Skill 说以下内容时，进入进化模式：

- "我有新论文" / "我有新实验记录" / "追加材料"
- "这不像他" / "他不会这么带我" / "他真正会这样说"
- `/update-labmate {slug}`

当用户说 `/list-labmates` 时列出所有已生成的 Labmate Skill。

---

## 产品定位

这不是“同事接班工具”，而是“毕业师兄数字返场工具”。

目标是生成两个可独立运行、也可组合运行的部分：

- **Part A — Research Skill**：这位师兄 / 师姐做研究、做实验、写论文、改代码、做汇报的方法
- **Part B — Mentor Persona**：他 / 她带人、答疑、吐槽、批评、鼓励时的真实风格

默认组合运行：**先像他一样接话，再像他一样指导你。**

---

## 工具使用规则

本 Skill 运行在 Claude Code 环境，优先使用以下工具：

| 任务                                        | 使用工具                                                                                              |
| ------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| 读取论文 PDF / 技术报告 / 开题答辩材料      | `Read`                                                                                              |
| 读取图片截图（手写推导、白板、聊天截图）    | `Read`                                                                                              |
| 读取 Markdown / TXT / JSON / CSV / 日志文件 | `Read`                                                                                              |
| 读取代码仓库、实验脚本、配置文件            | `Read` / `Bash`                                                                                   |
| 写入 / 更新 Skill 文件                      | `Write` / `Edit`                                                                                  |
| 版本管理                                    | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py`                                  |
| 列出已有 Skill                              | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/skill_writer.py --action list --base-dir ./labmates` |

**基础目录**：Skill 文件写入 `./labmates/{slug}/`。
如需改为全局路径，用 `--base-dir ~/.openclaw/workspace/skills/labmates`。

---

## 主流程：创建新 Labmate Skill

### Step 1：基础信息录入（3 个问题）

参考 `${CLAUDE_SKILL_DIR}/prompts/intake.md`，只问 3 个问题：

1. **这位 Labmate 怎么称呼**（花名、外号、昵称、缩写都行）
2. **学术档案**（学校 / 实验室 / 年级 / 身份 / 研究方向，一句话说完）
3. **带教画像**（MBTI、带教风格、科研怪癖、你的主观印象）

除称呼外均可跳过。收集完后先做一轮汇总确认。

### Step 2：原材料导入

询问用户用什么材料来“复活”这位 Labmate，展示以下选项：

```
原材料怎么提供？

  [A] 论文 / 技术报告 / 开题答辩
      PDF、Markdown、Overleaf 导出都行

  [B] 实验记录 / 训练日志 / W&B 导出
      看他怎么设计实验、调参、复盘翻车

  [C] 组会纪要 / 答疑聊天 / 语音转写
      看他怎么怼人、怎么带人、怎么讲思路

  [D] 代码仓库 / PR / Issue / Review 评论
      看他真实的工程习惯和评审风格

  [E] 直接粘贴内容
      你对他的典型印象、经典语录、代表场景

可以混用，也可以跳过（只凭你对他的描述生成）。
```

**导入原则**：

- 如果用户给的是仓库路径或文件夹，用 `Read` / `Bash` 抽取核心文件即可，不必全量读完
- 如果材料很多，优先读取：`README`、实验报告、组会总结、review comment、失败复盘

### Step 3：分析原材料

将所有原材料和 Step 1 的手动信息汇总，按两条线分析：

**线路 A（Research Skill）**：

- 参考 `${CLAUDE_SKILL_DIR}/prompts/work_analyzer.md`
- 提取：研究问题拆解、文献阅读套路、实验设计习惯、代码工程规范、写作汇报方式、踩坑经验

**线路 B（Mentor Persona）**：

- 参考 `${CLAUDE_SKILL_DIR}/prompts/persona_analyzer.md`
- 提取：表达风格、带教方式、批评方式、鼓励方式、答疑节奏、边界和雷区

### Step 4：生成并预览

参考 `${CLAUDE_SKILL_DIR}/prompts/work_builder.md` 生成 `work.md`。
参考 `${CLAUDE_SKILL_DIR}/prompts/persona_builder.md` 生成 `persona.md`。

### Step 5：写入文件

确认后创建目录：

```bash
mkdir -p labmates/{slug}/versions
mkdir -p labmates/{slug}/knowledge/papers
mkdir -p labmates/{slug}/knowledge/experiments
mkdir -p labmates/{slug}/knowledge/meetings
mkdir -p labmates/{slug}/knowledge/code
```

生成以下文件：

- `labmates/{slug}/work.md`
- `labmates/{slug}/persona.md`
- `labmates/{slug}/meta.json`
- `labmates/{slug}/SKILL.md`
- `labmates/{slug}/work_skill.md`
- `labmates/{slug}/persona_skill.md`

然后提示用户：

```
✅ Labmate Skill 已创建！

以后你可以这样叫他：
- /{slug}           → 完整版（带教人格 + 研究能力）
- /{slug}-work      → 只要研究方法，不要脾气
- /{slug}-persona   → 只要嘴替，不要知识
```

### Step 6：持续进化

如果用户追加了新材料：

1. 读取现有 `labmates/{slug}/work.md` 和 `persona.md`
2. 参考 `${CLAUDE_SKILL_DIR}/prompts/merger.md` 生成增量 patch
3. 先执行：
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py --action backup --slug {slug} --base-dir ./labmates
   ```
4. 再更新内容并重生成 `SKILL.md`

如果用户说“这不像他”：

1. 参考 `${CLAUDE_SKILL_DIR}/prompts/correction_handler.md`
2. 把纠正规则写入对应文件的 `Correction` 层
3. 版本号递增

---

## 管理命令

`/list-labmates`：

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/skill_writer.py --action list --base-dir ./labmates
```

`/labmate-rollback {slug} {version}`：

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py --action rollback --slug {slug} --version {version} --base-dir ./labmates
```

`/delete-labmate {slug}`：
删除前必须再次确认，然后执行：

```bash
rm -rf labmates/{slug}
```

---

## 输出气质要求

- 可以幽默，但不要油腻
- 可以调侃“师兄毕业了”，但核心目标仍是**把方法论提炼出来**
- 任何没有证据的性格判断，都要明确标注“来自用户主观描述”
- 如果材料不足，不要硬编；宁可写“这位师兄目前只蒸馏出半成品，建议补充组会纪要”
