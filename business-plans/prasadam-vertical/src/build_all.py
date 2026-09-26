"""Rebuild every deliverable from content.py."""
import runpy
from pathlib import Path

HERE = Path(__file__).resolve().parent
for script in ("build_docs.py", "build_deck.py", "build_tracker.py", "build_mindmap.py"):
    runpy.run_path(str(HERE / script), run_name="__main__")
