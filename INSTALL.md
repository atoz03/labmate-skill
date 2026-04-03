# labmate.skill 安装说明

推荐使用仓库名 `labmate-skill`，与命令 `/create-labmate`、输出目录 `./labmates/` 保持一致。

---

## 1. 安装到 Claude Code

在你的项目目录下：

```bash
git clone https://github.com/<your-account>/labmate-skill .claude/skills/create-labmate
```

或安装到全局目录：

```bash
git clone https://github.com/<your-account>/labmate-skill ~/.claude/skills/create-labmate
```

安装完成后，在 Claude Code 中输入：

```bash
/create-labmate
```

即可启动。

生成的 Skill 默认写入：

```
./labmates/
```

---

## 2. 安装到 OpenClaw / 兼容 AgentSkills 环境

```bash
git clone https://github.com/<your-account>/labmate-skill ~/.openclaw/workspace/skills/create-labmate
```

重启 session 后，说：

```bash
/create-labmate
```

---

## 3. 可选依赖

```bash
pip3 install -r requirements.txt
```

主要用途：

- `pypinyin`：把中文昵称转成 slug
- 部分解析脚本的兼容依赖

不安装也能跑主流程，只是 slug 转换可能退化。

---

## 4. 推荐准备的材料

最推荐的原材料清单：

- 论文 PDF / technical report
- 开题 / 中期 / 答辩 slides
- 实验日志 / 调参记录 / 失败复盘
- 组会纪要 / 答疑聊天 / 语音转写
- 仓库 README / 实验脚本 / PR / review comment

对这个 Skill 来说，**能体现研究方法和带教风格的材料，价值远高于流水账聊天。**

---

## 5. 快速验证

安装后，可以直接跑：

```bash
python3 tools/skill_writer.py --action list --base-dir ./labmates
```

如果没有任何生成结果，你会看到：

```
暂无已创建的 Labmate Skill
```

---

## 6. 管理命令

### 列出已有 Labmate Skill

```bash
python3 tools/skill_writer.py --action list --base-dir ./labmates
```

### 查看某个 Skill 的历史版本

```bash
python3 tools/version_manager.py --action list --slug qing-yun --base-dir ./labmates
```

### 手动备份当前版本

```bash
python3 tools/version_manager.py --action backup --slug qing-yun --base-dir ./labmates
```

### 回滚到指定版本

```bash
python3 tools/version_manager.py --action rollback --slug qing-yun --version v2 --base-dir ./labmates
```

---

## 7. 目录结构说明

```
labmate-skill/
├── SKILL.md
├── prompts/
├── tools/
├── docs/
└── labmates/
    └── {slug}/
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
