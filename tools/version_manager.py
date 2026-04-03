#!/usr/bin/env python3
"""Labmate Skill 版本管理器。"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

MAX_VERSIONS = 10
SNAPSHOT_FILES = ("SKILL.md", "work.md", "persona.md", "work_skill.md", "persona_skill.md", "meta.json")


def list_versions(skill_dir: Path) -> list[dict]:
    versions_dir = skill_dir / "versions"
    if not versions_dir.exists():
        return []
    versions = []
    for version_dir in sorted(versions_dir.iterdir(), key=lambda item: item.stat().st_mtime):
        if not version_dir.is_dir():
            continue
        files = [f.name for f in version_dir.iterdir() if f.is_file()]
        archived_at = datetime.fromtimestamp(version_dir.stat().st_mtime, tz=timezone.utc).strftime("%Y-%m-%d %H:%M")
        versions.append({"version": version_dir.name, "archived_at": archived_at, "files": files, "path": str(version_dir)})
    return versions


def backup_current_version(skill_dir: Path, version_name: str | None = None) -> str:
    meta_path = skill_dir / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
    current_version = meta.get("version", "v1")
    snapshot_name = version_name or f"{current_version}_manual_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
    backup_dir = skill_dir / "versions" / snapshot_name
    backup_dir.mkdir(parents=True, exist_ok=True)
    for filename in SNAPSHOT_FILES:
        src = skill_dir / filename
        if src.exists():
            shutil.copy2(src, backup_dir / filename)
    return snapshot_name


def rollback(skill_dir: Path, target_version: str) -> bool:
    version_dir = skill_dir / "versions" / target_version
    if not version_dir.exists():
        print(f"错误：版本 {target_version} 不存在", file=sys.stderr)
        return False
    meta_path = skill_dir / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
    current_version = meta.get("version", "v?")
    backup_name = backup_current_version(skill_dir, f"{current_version}_before_rollback")
    restored_files = []
    for filename in SNAPSHOT_FILES:
        src = version_dir / filename
        if src.exists():
            shutil.copy2(src, skill_dir / filename)
            restored_files.append(filename)
    if meta_path.exists():
        latest_meta = json.loads(meta_path.read_text(encoding="utf-8"))
        latest_meta["version"] = target_version + "_restored"
        latest_meta["updated_at"] = datetime.now(timezone.utc).isoformat()
        latest_meta["rollback_from"] = current_version
        latest_meta["rollback_backup"] = backup_name
        meta_path.write_text(json.dumps(latest_meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"已回滚到 {target_version}，恢复文件：{', '.join(restored_files)}")
    return True


def cleanup_old_versions(skill_dir: Path, max_versions: int = MAX_VERSIONS) -> None:
    versions_dir = skill_dir / "versions"
    if not versions_dir.exists():
        return
    version_dirs = sorted([item for item in versions_dir.iterdir() if item.is_dir()], key=lambda item: item.stat().st_mtime)
    stale_dirs = version_dirs[:-max_versions] if len(version_dirs) > max_versions else []
    for old_dir in stale_dirs:
        shutil.rmtree(old_dir)
        print(f"已清理旧版本：{old_dir.name}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Labmate Skill 版本管理器")
    parser.add_argument("--action", required=True, choices=["list", "backup", "rollback", "cleanup"])
    parser.add_argument("--slug", required=True, help="Labmate slug")
    parser.add_argument("--version", help="目标版本号（rollback 时使用）")
    parser.add_argument("--base-dir", default="~/.openclaw/workspace/skills/labmates", help="Labmate Skill 根目录")
    args = parser.parse_args()
    base_dir = Path(args.base_dir).expanduser()
    skill_dir = base_dir / args.slug
    if not skill_dir.exists():
        print(f"错误：找不到 Skill 目录 {skill_dir}", file=sys.stderr)
        sys.exit(1)
    if args.action == "list":
        versions = list_versions(skill_dir)
        if not versions:
            print(f"{args.slug} 暂无历史版本")
            return
        print(f"{args.slug} 的历史版本：\n")
        for version in versions:
            print(f"  {version['version']}  存档时间: {version['archived_at']}  文件: {', '.join(version['files'])}")
        return
    if args.action == "backup":
        snapshot_name = backup_current_version(skill_dir)
        print(f"已手动备份当前版本：{snapshot_name}")
        return
    if args.action == "rollback":
        if not args.version:
            print("错误：rollback 操作需要 --version", file=sys.stderr)
            sys.exit(1)
        rollback(skill_dir, args.version)
        return
    cleanup_old_versions(skill_dir)
    print("清理完成")


if __name__ == "__main__":
    main()
