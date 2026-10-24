#!/usr/bin/env python3
"""Convert a claude.ai data export into Markdown files Claude Code can read.

claude.ai has no "move this chat to Claude Code" button. What it does have is
Settings > Privacy > Export data, which emails you a zip containing
``conversations.json`` (every chat) and ``projects.json`` (project
instructions and knowledge files). This script turns that export into one
Markdown file per conversation, plus an index, inside this repository, so any
Claude Code session can grep, read and build on them.

Usage
-----
    # Point it at the zip, the extracted folder, or conversations.json directly
    python3 scripts/import_claude_chats.py ~/Downloads/data-2026-10-24.zip
    python3 scripts/import_claude_chats.py ~/Downloads/export-folder
    python3 scripts/import_claude_chats.py conversations.json --out docs/claude-chats

    # Only chats whose title matches (case-insensitive substring or regex)
    python3 scripts/import_claude_chats.py export.zip --match yatra --match "vendor|rate"

    # Only chats updated on/after a date
    python3 scripts/import_claude_chats.py export.zip --since 2026-06-01

Output layout (default --out docs/claude-chats):
    INDEX.md                      one row per chat, newest first
    chats/<date>-<slug>.md        the conversation, human/assistant turns
    projects/<slug>/README.md     project description + instructions
    projects/<slug>/<file>        project knowledge files, verbatim

Re-running is safe: files are rewritten from the export, nothing else in the
output folder is touched. Review the output before committing; chats can
contain personal details that do not belong in git.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

MAX_SLUG = 60


# --------------------------------------------------------------------------- #
# Locating the export
# --------------------------------------------------------------------------- #

def locate_export(source: Path) -> tuple[Path | None, Path | None, tempfile.TemporaryDirectory | None]:
    """Return (conversations.json, projects.json, tempdir) for a zip, dir or file."""
    tmp: tempfile.TemporaryDirectory | None = None

    if source.is_file() and source.suffix.lower() == ".zip":
        tmp = tempfile.TemporaryDirectory(prefix="claude-export-")
        with zipfile.ZipFile(source) as zf:
            for member in zf.namelist():
                # Guard against path traversal inside an untrusted archive.
                dest = (Path(tmp.name) / member).resolve()
                if not str(dest).startswith(str(Path(tmp.name).resolve())):
                    raise SystemExit(f"refusing to extract suspicious path: {member}")
            zf.extractall(tmp.name)
        root = Path(tmp.name)
    elif source.is_file():
        name = source.name.lower()
        if name == "projects.json":
            return None, source, None
        return source, (source.parent / "projects.json" if (source.parent / "projects.json").exists() else None), None
    elif source.is_dir():
        root = source
    else:
        raise SystemExit(f"not found: {source}")

    conv = next(iter(root.rglob("conversations.json")), None)
    proj = next(iter(root.rglob("projects.json")), None)
    if conv is None and proj is None:
        raise SystemExit(f"no conversations.json or projects.json found under {root}")
    return conv, proj, tmp


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def parse_ts(value: Any) -> datetime | None:
    if not value or not isinstance(value, str):
        return None
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def fmt_ts(dt: datetime | None) -> str:
    return dt.strftime("%Y-%m-%d %H:%M UTC") if dt else "unknown"


def slugify(text: str, fallback: str) -> str:
    text = re.sub(r"[^\w\s-]", "", (text or "").lower(), flags=re.UNICODE)
    text = re.sub(r"[\s_-]+", "-", text).strip("-")
    text = text[:MAX_SLUG].rstrip("-")
    return text or fallback


def message_text(msg: dict[str, Any]) -> str:
    """Flatten a message into Markdown text.

    Newer exports carry a ``content`` list of typed blocks; older ones only a
    ``text`` string. Prefer the blocks when they are present and non-empty.
    """
    parts: list[str] = []
    blocks = msg.get("content")
    if isinstance(blocks, list):
        for block in blocks:
            if not isinstance(block, dict):
                continue
            btype = block.get("type")
            if btype == "text" and block.get("text"):
                parts.append(str(block["text"]))
            elif btype == "tool_use":
                name = block.get("name", "tool")
                parts.append(f"_[tool call: {name}]_")
            elif btype == "tool_result":
                parts.append("_[tool result omitted]_")
    if not parts and msg.get("text"):
        parts.append(str(msg["text"]))

    for att in msg.get("attachments") or []:
        if not isinstance(att, dict):
            continue
        fname = att.get("file_name") or att.get("filename") or "attachment"
        extracted = att.get("extracted_content")
        if extracted:
            parts.append(f"\n**Attachment: {fname}**\n\n```\n{extracted}\n```")
        else:
            parts.append(f"_[attachment: {fname}]_")
    for f in msg.get("files") or []:
        if isinstance(f, dict) and f.get("file_name"):
            parts.append(f"_[file: {f['file_name']}]_")

    return "\n\n".join(p.strip() for p in parts if p and p.strip())


def wants(name: str, patterns: list[re.Pattern[str]]) -> bool:
    return not patterns or any(p.search(name or "") for p in patterns)


def unique_path(folder: Path, stem: str, suffix: str, taken: set[str]) -> Path:
    candidate = stem
    n = 2
    while candidate in taken:
        candidate = f"{stem}-{n}"
        n += 1
    taken.add(candidate)
    return folder / f"{candidate}{suffix}"


# --------------------------------------------------------------------------- #
# Conversations
# --------------------------------------------------------------------------- #

def convert_conversations(
    path: Path, out: Path, patterns: list[re.Pattern[str]], since: datetime | None
) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and "conversations" in data:
        data = data["conversations"]
    if not isinstance(data, list):
        raise SystemExit("conversations.json is not a list of conversations")

    chats_dir = out / "chats"
    chats_dir.mkdir(parents=True, exist_ok=True)
    taken: set[str] = set()
    rows: list[dict[str, Any]] = []
    skipped = 0

    for conv in data:
        if not isinstance(conv, dict):
            continue
        name = (conv.get("name") or "").strip() or "Untitled chat"
        created = parse_ts(conv.get("created_at"))
        updated = parse_ts(conv.get("updated_at")) or created
        messages = [m for m in (conv.get("chat_messages") or []) if isinstance(m, dict)]

        if not wants(name, patterns) or (since and updated and updated < since):
            skipped += 1
            continue

        messages.sort(key=lambda m: parse_ts(m.get("created_at")) or datetime.min.replace(tzinfo=timezone.utc))
        date_prefix = (created or updated or datetime.now(timezone.utc)).strftime("%Y-%m-%d")
        uuid = str(conv.get("uuid") or "")
        stem = f"{date_prefix}-{slugify(name, uuid[:8] or 'chat')}"
        target = unique_path(chats_dir, stem, ".md", taken)

        lines = [
            f"# {name}",
            "",
            f"- Source: claude.ai chat export",
            f"- Conversation id: `{uuid or 'unknown'}`",
            f"- Created: {fmt_ts(created)}",
            f"- Updated: {fmt_ts(updated)}",
            f"- Messages: {len(messages)}",
        ]
        if conv.get("project_uuid") or (conv.get("project") or {}).get("name"):
            pname = (conv.get("project") or {}).get("name") or conv.get("project_uuid")
            lines.append(f"- Project: {pname}")
        if conv.get("summary"):
            lines += ["", "## Summary", "", str(conv["summary"]).strip()]
        lines += ["", "## Conversation", ""]

        for msg in messages:
            sender = msg.get("sender") or msg.get("role") or "unknown"
            label = {"human": "You", "user": "You", "assistant": "Claude"}.get(sender, sender.title())
            body = message_text(msg) or "_(empty)_"
            lines += [f"### {label} · {fmt_ts(parse_ts(msg.get('created_at')))}", "", body, ""]

        target.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
        rows.append(
            {
                "name": name,
                "file": target.relative_to(out).as_posix(),
                "created": created,
                "updated": updated,
                "messages": len(messages),
            }
        )

    print(f"conversations: wrote {len(rows)}, skipped {skipped} (filters)", file=sys.stderr)
    return rows


# --------------------------------------------------------------------------- #
# Projects
# --------------------------------------------------------------------------- #

def convert_projects(path: Path, out: Path, patterns: list[re.Pattern[str]]) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and "projects" in data:
        data = data["projects"]
    if not isinstance(data, list):
        raise SystemExit("projects.json is not a list of projects")

    projects_dir = out / "projects"
    taken: set[str] = set()
    rows: list[dict[str, Any]] = []

    for proj in data:
        if not isinstance(proj, dict):
            continue
        name = (proj.get("name") or "").strip() or "Untitled project"
        if not wants(name, patterns):
            continue
        folder = unique_path(projects_dir, slugify(name, str(proj.get("uuid") or "project")[:8]), "", taken)
        folder.mkdir(parents=True, exist_ok=True)

        lines = [f"# Project: {name}", ""]
        if proj.get("description"):
            lines += [str(proj["description"]).strip(), ""]
        lines += [
            f"- Source: claude.ai project export",
            f"- Project id: `{proj.get('uuid') or 'unknown'}`",
            f"- Created: {fmt_ts(parse_ts(proj.get('created_at')))}",
            f"- Updated: {fmt_ts(parse_ts(proj.get('updated_at')))}",
        ]
        if proj.get("prompt_template"):
            lines += ["", "## Instructions", "", str(proj["prompt_template"]).strip()]

        docs = [d for d in (proj.get("docs") or []) if isinstance(d, dict)]
        if docs:
            lines += ["", "## Knowledge files", ""]
        doc_taken: set[str] = set()
        for doc in docs:
            fname = doc.get("filename") or "document.txt"
            safe = Path(fname).name  # strip any directory component from the export
            stem, suffix = Path(safe).stem, Path(safe).suffix or ".txt"
            target = unique_path(folder, slugify(stem, "document"), suffix, doc_taken)
            target.write_text(str(doc.get("content") or ""), encoding="utf-8")
            lines.append(f"- [{safe}]({target.name})")

        (folder / "README.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
        rows.append({"name": name, "file": (folder / "README.md").relative_to(out).as_posix(), "docs": len(docs)})

    print(f"projects: wrote {len(rows)}", file=sys.stderr)
    return rows


# --------------------------------------------------------------------------- #
# Index
# --------------------------------------------------------------------------- #

def write_index(out: Path, chats: list[dict[str, Any]], projects: list[dict[str, Any]]) -> None:
    chats.sort(key=lambda r: r["updated"] or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
    lines = [
        "# Claude chat archive",
        "",
        "Generated by `scripts/import_claude_chats.py` from a claude.ai data export.",
        f"Last run: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}.",
        "",
    ]
    if projects:
        lines += ["## Projects", "", "| Project | Knowledge files |", "| --- | --- |"]
        lines += [f"| [{p['name']}]({p['file']}) | {p['docs']} |" for p in projects]
        lines.append("")
    lines += [
        f"## Chats ({len(chats)})",
        "",
        "| Updated | Chat | Messages |",
        "| --- | --- | --- |",
    ]
    for r in chats:
        when = r["updated"].strftime("%Y-%m-%d") if r["updated"] else "unknown"
        title = r["name"].replace("|", "\\|")
        lines.append(f"| {when} | [{title}]({r['file']}) | {r['messages']} |")
    (out / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- #

def main(argv: Iterable[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", type=Path, help="export .zip, extracted folder, or conversations.json")
    ap.add_argument("--out", type=Path, default=Path("docs/claude-chats"), help="output folder (default: docs/claude-chats)")
    ap.add_argument("--match", action="append", default=[], metavar="PATTERN",
                    help="only chats/projects whose title matches this regex (case-insensitive); repeatable")
    ap.add_argument("--since", type=str, default=None, metavar="YYYY-MM-DD",
                    help="only chats updated on or after this date")
    ap.add_argument("--no-projects", action="store_true", help="skip projects.json even if present")
    args = ap.parse_args(list(argv) if argv is not None else None)

    patterns = [re.compile(p, re.IGNORECASE) for p in args.match]
    since = None
    if args.since:
        try:
            since = datetime.strptime(args.since, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        except ValueError:
            ap.error("--since must be YYYY-MM-DD")

    conv_path, proj_path, tmp = locate_export(args.source)
    try:
        args.out.mkdir(parents=True, exist_ok=True)
        chats = convert_conversations(conv_path, args.out, patterns, since) if conv_path else []
        projects = convert_projects(proj_path, args.out, patterns) if (proj_path and not args.no_projects) else []
        write_index(args.out, chats, projects)
        print(f"index: {args.out / 'INDEX.md'}", file=sys.stderr)
    finally:
        if tmp:
            tmp.cleanup()
    return 0


if __name__ == "__main__":
    sys.exit(main())
