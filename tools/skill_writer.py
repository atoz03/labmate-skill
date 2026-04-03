#!/usr/bin/env python3
"""Labmate Skill 文件写入器。"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

SKILL_MD_TEMPLATE = """\
---
name: labmate_{slug}
description: {name}，{identity}
user-invocable: true
---

# {name}

{identity}

---

## PART A：Research Skill

{work_content}

---

## PART B：Mentor Persona

{persona_content}

---

## 运行规则

1. 先由 PART B 决定语气和带教姿势
2. 再由 PART A 给出研究方法与执行建议
3. 输出时保持 PART B 的说话风格
4. 不知道就明确说不知道，并给出下一步验证路径

**Correction 规则优先级最高。**
"""


def slugify(name: str) -> str:
    try:
        from pypinyin import lazy_pinyin
        slug = "-".join(lazy_pinyin(name))
    except ImportError:
        result = []
        for char in name.lower():
            if char.isascii() and (char.isalnum() or char in ("-", "_")):
                result.append(char)
            elif char.isspace():
                result.append("-")
        slug = "".join(result)
    slug = slug.replace("_", "-")
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug or "labmate"


def build_identity_string(meta: dict) -> str:
    profile = meta.get("profile", {})
    parts = [
        profile.get("school", ""),
        profile.get("lab", ""),
        profile.get("cohort", ""),
        profile.get("role", ""),
    ]
    parts = [part for part in parts if part]
    identity = " / ".join(parts) if parts else "你的 Labmate"
    field = profile.get("field", "")
    if field:
        identity += f"，方向：{field}"
    mbti = profile.get("mbti", "")
    if mbti:
        identity += f"，MBTI {mbti}"
    return identity


def build_sub_skill(name: str, slug: str, skill_type: str, description: str, content: str) -> str:
    return (
        f"---\nname: labmate_{slug}_{skill_type}\n"
        f"description: {name} 的{description}\n"
        f"user-invocable: true\n---\n\n{content}\n"
    )


def create_skill(base_dir: Path, slug: str, meta: dict, work_content: str, persona_content: str) -> Path:
    skill_dir = base_dir / slug
    skill_dir.mkdir(parents=True, exist_ok=True)
    for subdir in ("versions", "knowledge/papers", "knowledge/experiments", "knowledge/meetings", "knowledge/code"):
        (skill_dir / subdir).mkdir(parents=True, exist_ok=True)
    (skill_dir / "work.md").write_text(work_content, encoding="utf-8")
    (skill_dir / "persona.md").write_text(persona_content, encoding="utf-8")
    name = meta.get("name", slug)
    identity = build_identity_string(meta)
    (skill_dir / "SKILL.md").write_text(
        SKILL_MD_TEMPLATE.format(
            slug=slug,
            name=name,
            identity=identity,
            work_content=work_content,
            persona_content=persona_content,
        ),
        encoding="utf-8",
    )
    (skill_dir / "work_skill.md").write_text(
        build_sub_skill(name, slug, "work", "研究能力（仅 Work，无 Persona）", work_content),
        encoding="utf-8",
    )
    (skill_dir / "persona_skill.md").write_text(
        build_sub_skill(name, slug, "persona", "带教人格（仅 Persona，无 Work）", persona_content),
        encoding="utf-8",
    )
    now = datetime.now(timezone.utc).isoformat()
    meta["slug"] = slug
    meta.setdefault("created_at", now)
    meta["updated_at"] = now
    meta["version"] = "v1"
    meta.setdefault("corrections_count", 0)
    (skill_dir / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    return skill_dir


def update_skill(skill_dir: Path, work_patch: Optional[str] = None, persona_patch: Optional[str] = None, correction: Optional[dict] = None) -> str:
    meta_path = skill_dir / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    current_version = meta.get("version", "v1")
    try:
        version_num = int(current_version.lstrip("v").split("_")[0]) + 1
    except ValueError:
        version_num = 2
    new_version = f"v{version_num}"
    version_dir = skill_dir / "versions" / current_version
    version_dir.mkdir(parents=True, exist_ok=True)
    for fname in ("SKILL.md", "work.md", "persona.md", "work_skill.md", "persona_skill.md", "meta.json"):
        src = skill_dir / fname
        if src.exists():
            shutil.copy2(src, version_dir / fname)
    if work_patch:
        current_work = (skill_dir / "work.md").read_text(encoding="utf-8")
        (skill_dir / "work.md").write_text(current_work.rstrip() + "\n\n" + work_patch.strip() + "\n", encoding="utf-8")
    if persona_patch or correction:
        current_persona = (skill_dir / "persona.md").read_text(encoding="utf-8")
        if correction:
            correction_line = f"- [场景：{correction.get('scene', '通用')}] 不应该 {correction['wrong']}，应该 {correction['correct']}"
            target = "## Correction 记录"
            if target in current_persona:
                head, tail = current_persona.split(target, 1)
                tail = tail.replace("（暂无记录）", "", 1).lstrip("\n")
                new_persona = f"{head}{target}\n\n{correction_line}\n"
                if tail.strip():
                    new_persona += "\n" + tail.lstrip("\n")
            else:
                new_persona = current_persona.rstrip() + f"\n\n## Correction 记录\n\n{correction_line}\n"
            meta["corrections_count"] = meta.get("corrections_count", 0) + 1
        else:
            new_persona = current_persona.rstrip() + "\n\n" + persona_patch.strip() + "\n"
        (skill_dir / "persona.md").write_text(new_persona, encoding="utf-8")
    work_content = (skill_dir / "work.md").read_text(encoding="utf-8")
    persona_content = (skill_dir / "persona.md").read_text(encoding="utf-8")
    name = meta.get("name", skill_dir.name)
    identity = build_identity_string(meta)
    (skill_dir / "SKILL.md").write_text(
        SKILL_MD_TEMPLATE.format(
            slug=skill_dir.name,
            name=name,
            identity=identity,
            work_content=work_content,
            persona_content=persona_content,
        ),
        encoding="utf-8",
    )
    (skill_dir / "work_skill.md").write_text(
        build_sub_skill(name, skill_dir.name, "work", "研究能力（仅 Work，无 Persona）", work_content),
        encoding="utf-8",
    )
    (skill_dir / "persona_skill.md").write_text(
        build_sub_skill(name, skill_dir.name, "persona", "带教人格（仅 Persona，无 Work）", persona_content),
        encoding="utf-8",
    )
    meta["version"] = new_version
    meta["updated_at"] = datetime.now(timezone.utc).isoformat()
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    return new_version


def list_labmates(base_dir: Path) -> list[dict]:
    results = []
    if not base_dir.exists():
        return results
    for skill_dir in sorted(base_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        meta_path = skill_dir / "meta.json"
        if not meta_path.exists():
            continue
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        results.append({
            "slug": meta.get("slug", skill_dir.name),
            "name": meta.get("name", skill_dir.name),
            "identity": build_identity_string(meta),
            "version": meta.get("version", "v1"),
            "updated_at": meta.get("updated_at", ""),
            "corrections_count": meta.get("corrections_count", 0),
        })
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Labmate Skill 文件写入器")
    parser.add_argument("--action", required=True, choices=["create", "update", "list"])
    parser.add_argument("--slug", help="Labmate slug")
    parser.add_argument("--name", help="Labmate 称呼")
    parser.add_argument("--meta", help="meta.json 文件路径")
    parser.add_argument("--work", help="work.md 内容文件路径")
    parser.add_argument("--persona", help="persona.md 内容文件路径")
    parser.add_argument("--work-patch", help="work.md 增量更新内容文件路径")
    parser.add_argument("--persona-patch", help="persona.md 增量更新内容文件路径")
    parser.add_argument("--base-dir", default="./labmates", help="Labmate Skill 根目录（默认：./labmates）")
    args = parser.parse_args()
    base_dir = Path(args.base_dir).expanduser()

    if args.action == "list":
        items = list_labmates(base_dir)
        if not items:
            print("暂无已创建的 Labmate Skill")
            return
        print(f"已创建 {len(items)} 个 Labmate Skill：\n")
        for item in items:
            updated = item["updated_at"][:10] if item["updated_at"] else "未知"
            print(f"  [{item['slug']}]  {item['name']} — {item['identity']}")
            print(f"    版本: {item['version']}  纠正次数: {item['corrections_count']}  更新: {updated}")
            print()
        return

    if args.action == "create":
        if not args.slug and not args.name:
            print("错误：create 操作需要 --slug 或 --name", file=sys.stderr)
            sys.exit(1)
        meta = json.loads(Path(args.meta).read_text(encoding="utf-8")) if args.meta else {}
        if args.name:
            meta["name"] = args.name
        slug = args.slug or slugify(meta.get("name", "labmate"))
        work_content = Path(args.work).read_text(encoding="utf-8") if args.work else ""
        persona_content = Path(args.persona).read_text(encoding="utf-8") if args.persona else ""
        skill_dir = create_skill(base_dir, slug, meta, work_content, persona_content)
        print(f"✅ Labmate Skill 已创建：{skill_dir}")
        print(f"   触发词：/{slug}")
        return

    if not args.slug:
        print("错误：update 操作需要 --slug", file=sys.stderr)
        sys.exit(1)
    skill_dir = base_dir / args.slug
    if not skill_dir.exists():
        print(f"错误：找不到 Skill 目录 {skill_dir}", file=sys.stderr)
        sys.exit(1)
    work_patch = Path(args.work_patch).read_text(encoding="utf-8") if args.work_patch else None
    persona_patch = Path(args.persona_patch).read_text(encoding="utf-8") if args.persona_patch else None
    new_version = update_skill(skill_dir, work_patch, persona_patch)
    print(f"✅ Labmate Skill 已更新到 {new_version}：{skill_dir}")


if __name__ == "__main__":
    main()
