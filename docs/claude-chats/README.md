# Bringing claude.ai chats into Claude Code

claude.ai chat, Cowork and Claude Code each keep their own conversation
list, and there is no "move to Code" button. The reliable way to carry
important chats across is to export them, convert them to Markdown, and keep
them in this repository. Anything in the repo is visible to every Claude Code
session, whether local, cloud or desktop.

## One-time: export your chats

1. Open claude.ai in a browser and go to **Settings → Privacy → Export data**.
2. Click **Export data**. Anthropic emails you a download link; it expires
   after 24 hours, so download the zip promptly.
3. The zip contains `conversations.json` (all chats, with messages and
   attachments) and `projects.json` (project instructions and knowledge
   files).

## Convert into this folder

From the repository root:

```bash
# Everything
python3 scripts/import_claude_chats.py ~/Downloads/data-export.zip

# Only chats whose title mentions yatra, vendor or rate (regex, case-insensitive)
python3 scripts/import_claude_chats.py ~/Downloads/data-export.zip --match "yatra|vendor|rate"

# Only chats updated since a date
python3 scripts/import_claude_chats.py ~/Downloads/data-export.zip --since 2026-06-01
```

The script writes:

| Path | Contents |
| --- | --- |
| `INDEX.md` | One row per chat, newest first, linked to the file |
| `chats/<date>-<title>.md` | The full conversation, You / Claude turns, with attachment text inlined |
| `projects/<name>/README.md` | Project description and custom instructions |
| `projects/<name>/<file>` | Project knowledge files, verbatim |

Re-running overwrites the generated files from the new export and leaves
anything else in this folder alone.

## Before committing

Chats can carry phone numbers, personal addresses and bank details. Skim the
generated files, delete what should not be in git, then commit. If you want
the archive available to Claude Code but kept out of the repository history,
add `docs/claude-chats/chats/` to `.gitignore` and keep the files locally
only; cloud sessions will not see them in that case.

## Using the archive from Claude Code

Ask directly, for example:

- "Read docs/claude-chats/INDEX.md and list the chats about vendor rates."
- "Search docs/claude-chats for the Tirupati itinerary we discussed and put it into the itinerary table."
- "Summarise everything in docs/claude-chats about the finance approval process into docs/FINANCE.md."

`CLAUDE.md` at the repository root points Claude Code at this folder, so you
do not need to mention the path each time.

## Keeping it current

Export again whenever the chat side has gained important material (monthly is
a sensible rhythm), rerun the script, and commit. Chats that moved on will be
rewritten; new ones are added; the index is rebuilt.
