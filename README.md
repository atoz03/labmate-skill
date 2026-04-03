<div align="center">

# labmate.skill
> *"你们搞大模型的简直是码神，你们解放了前端兄弟，还要解放后端兄弟，测试兄弟，运维兄弟，解放网安兄弟，解放ic兄弟，最后解放自己解放全人类"*

> *"你为什么要追着你的老师兄/老师姐不放啊"*

**师兄师姐毕业了？别慌。把他蒸馏成 Skill，继续追问论文、实验和人生建议。**

</div>

---

## 这是什么

`labmate.skill` 是一个 meta-skill。

它服务于一个朴素而广泛存在的科研问题：

> **师兄师姐毕业了，但你的问题还没毕业。**

你给它喂：

- 论文 / 技术报告
- 实验记录 / 训练日志
- 组会纪要 / 答疑聊天
- 代码仓库 / PR / Review 评论
- 以及你对这位师兄 / 师姐的主观印象

它会帮你生成一个可调用的 **数字 Labmate**：

- **Research Skill**：像 TA 一样拆问题、做实验、改代码、写论文
- **Mentor Persona**：像 TA 一样说话、吐槽你、鼓励你、半夜回复“先把 appendix 看完”

适用于：

- 同事离职了，你要接锅
- 师兄毕业了，你要接方向
- 师姐不在了，你连实验环境都不知道谁配的
- 老板说“这个以前有人做过，你去继承一下”
---

## 核心能力

- 🎓 把“这块你去看我之前的实验”真正变成可调用资产
- 🔬 自动提取研究方法、实验套路、踩坑经验与补锅习惯
- 🗣️ 重建师兄 / 师姐的答疑风格：温柔型、毒舌型、问号型都行
- ♻️ 支持追加新材料，持续蒸馏，不怕 TA 毕业后还在偷偷进化
- 🕰️ 支持版本管理与回滚，防止把 2022 年的错误经验蒸馏成祖训

## 为什么需要它

因为实验室知识传承，长期依赖三种极不稳定的介质：

1. 师兄的口头禅  
2. 师姐的微信聊天记录  
3. 一台没人敢重装的服务器  

`labmate.skill` 的目标，就是把这些濒危科研资产，转成一个还能继续被追问的数字 Labmate。
---

## 安装

> **推荐仓库名：`labmate-skill`**

### Claude Code

```bash
git clone https://github.com/<your-account>/labmate-skill .claude/skills/create-labmate
```

或：

```bash
git clone https://github.com/<your-account>/labmate-skill ~/.claude/skills/create-labmate
```

### OpenClaw / 兼容 AgentSkills 环境

```bash
git clone https://github.com/<your-account>/labmate-skill ~/.openclaw/workspace/skills/create-labmate
```

> 可选依赖：
>
> ```bash
> pip3 install -r requirements.txt
> ```
>
> 主要用于 `pypinyin` 等辅助能力，不装也能运行。

---

## 使用

在 Claude Code 中输入：

```bash
/create-labmate
```

然后按提示提供：
- 这位 Labmate 的称呼
- 学校 / 实验室 / 年级 / 方向
- 带教画像
- 论文、实验日志、组会纪要、代码仓库等材料

完成后，你就可以这样调用：

- `/{slug}`：完整版（人格 + 研究能力）
- `/{slug}-work`：只要方法论，不要脾气
- `/{slug}-persona`：只要语气和带教风格

### 管理命令

- `/list-labmates`：列出所有已生成的 Labmate Skill
- `/labmate-rollback {slug} {version}`：回滚到历史版本
- `/delete-labmate {slug}`：删除指定 Skill（需再次确认）

---

## 适合喂什么材料

强烈推荐优先级：

1. **论文 / technical report / 开题答辩**
2. **实验记录 / 调参复盘 / 训练日志**
3. **组会纪要 / 答疑聊天 / 语音转写**
4. **代码仓库 / PR / Issue / Review comment**
5. **你对他的主观描述**

如果只能提供一种材料，我推荐：

> **组会纪要 + 实验复盘**

这是最容易同时蒸出“脑子”和“嘴”的组合。

---

## 目录结构

```
labmate-skill/
├── SKILL.md                # create-labmate 主入口
├── prompts/                # 分析与生成模板
├── tools/                  # 文件写入与版本管理脚本
├── docs/                   # 产品文档
└── labmates/               # 生成的 Labmate Skills（默认 gitignore）
    └── {slug}/
        ├── SKILL.md
        ├── work.md
        ├── persona.md
        ├── work_skill.md
        ├── persona_skill.md
        ├── meta.json
        ├── versions/
        └── knowledge/
```

---

## 致谢

这个项目的灵感致谢 **[同事.skill](https://github.com/titanwings/colleague-skill)**。

可以把它理解成一次有意识的“场景迁移”：
- **同事.skill** 解决的是“同事走了，知识怎么接班”
- **labmate.skill** 解决的是“师兄毕业了，方法论怎么继续追问”
