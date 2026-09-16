#!/usr/bin/env python3
"""
Static check that every table, view, column and RPC referenced from src/data
exists in the database built by scripts/validate_db.sh.

PostgREST fails at runtime with a 400 for a misspelled column, which is exactly
the kind of bug that only shows up on the one screen nobody opened before the
demo. This catches it at build time instead.

    ./scripts/validate_db.sh && python3 scripts/check_queries.py
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

CONN = os.environ.get("CONN", "-h /var/tmp/yatrapg -p 5433 -U postgres")
DB = os.environ.get("DB", "yatra_validate")

SRC = Path("src/data")

# .from('table')                                 -> table must exist
FROM_RE = re.compile(r"\.from\(\s*'([a-z_0-9]+)'\s*\)")
# .eq('col', ...) / .order('col') / .contains('col', ...) etc.
COL_RE = re.compile(
    r"\.(?:eq|neq|gt|gte|lt|lte|like|ilike|is|in|contains|containedBy|overlaps|order|not)"
    r"\(\s*'([a-zA-Z_0-9]+)'"
)
RPC_RE = re.compile(r"\.rpc\(\s*'([a-z_0-9]+)'")
# .select('a, b, c') — bare column lists only; embedded resources are skipped
SELECT_RE = re.compile(r"\.select\(\s*'([^']*)'")


def psql(sql: str) -> list[str]:
    out = subprocess.run(
        ["psql", *CONN.split(), "-d", DB, "-At", "-c", sql],
        capture_output=True, text=True, check=True,
    )
    return [l for l in out.stdout.splitlines() if l]


def main() -> int:
    relations = set(psql(
        "select table_name from information_schema.tables where table_schema='public' "
        "union select table_name from information_schema.views where table_schema='public'"
    ))
    columns: dict[str, set[str]] = {}
    for row in psql(
        "select table_name || ':' || column_name from information_schema.columns "
        "where table_schema='public'"
    ):
        t, c = row.split(":", 1)
        columns.setdefault(t, set()).add(c)
    functions = set(psql(
        "select routine_name from information_schema.routines where routine_schema='public'"
    ))

    problems: list[str] = []

    for path in sorted(SRC.glob("*.ts")):
        text = path.read_text()
        # Split into statement-ish blocks so a column is checked against the
        # table named in the same chain, not against every table in the file.
        for block in re.split(r"(?=supabase\s*\n?\s*\.from|supabase\.from|supabase\.rpc)", text):
            tables = FROM_RE.findall(block)
            if not tables:
                for fn in RPC_RE.findall(block):
                    if fn not in functions:
                        problems.append(f"{path}: rpc '{fn}' does not exist")
                continue
            table = tables[0]
            if table not in relations:
                problems.append(f"{path}: relation '{table}' does not exist")
                continue
            known = columns.get(table, set())

            for col in COL_RE.findall(block):
                if col not in known:
                    problems.append(f"{path}: {table} has no column '{col}'")

            for sel in SELECT_RE.findall(block):
                if "(" in sel:      # embedded resource, e.g. vendors(id, name)
                    continue
                for piece in sel.split(","):
                    col = piece.strip()
                    if not col or col == "*":
                        continue
                    if col not in known:
                        problems.append(f"{path}: {table} select references '{col}'")

    if problems:
        print("query check FAILED")
        for p in problems:
            print(f"  {p}")
        return 1

    print(f"query check OK — {len(relations)} relations, {len(functions)} functions")
    return 0


if __name__ == "__main__":
    sys.exit(main())
