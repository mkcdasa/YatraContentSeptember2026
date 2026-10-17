# Multi-Agent Plan of Action

How the remaining Yatra Knowledge Base work is split across AI agents so that
each one works **independently and in parallel**, without overwriting another
agent's work, and with as little of your time as possible.

---

## 1. The five rules that make parallel work safe

Most of the work is in setting things up so agents never collide. These five
rules do that, and everything else in this plan builds on them.

1. **One agent, one lane, one set of folders.** Each agent owns specific folders
   (section 3). It may read anything, but it writes only to its own folders. Two
   agents never edit the same file at the same time, so there are no merge
   conflicts.
2. **One agent, one branch, one pull request per task.** Every task runs on its
   own branch (`agent/<lane>/<short-task-name>`) in its own cloud session.
   Nothing reaches `main` without a pull request. `main` is what Lovable deploys,
   so it stays clean.
3. **Contracts change in one place only.** The database schema, the RLS policies,
   `src/types/db.ts` and `src/data/` are the "contracts" every screen depends on.
   Only the **Database agent** changes them. Other agents that need a new column
   or query open a *contract request* issue and keep working on the parts that
   don't need it.
4. **Shared "hotspot" files are touched only at integration.** A few files are
   edited by almost every feature. Agents don't edit them. They describe the
   change they need in the PR description, and the Integrator applies it when
   merging:
   - `src/routes/AppRoutes.tsx` (new routes)
   - `src/pages/More.tsx` and `src/components/app/AppShell.tsx` (navigation)
   - `package.json` / `package-lock.json` (new dependencies)
5. **Same checks for every agent.** No PR is "done" until these pass:
   ```bash
   npm run typecheck
   npm run build
   ./scripts/validate_db.sh --rls      # only if supabase/ changed
   python3 scripts/check_queries.py    # only if src/data/ or supabase/ changed
   ```
   A GitHub Action runs them on every PR (Wave 0), so a broken PR is caught
   before you look at it.

---

## 2. Agent roster

| # | Agent | Mission | Runs |
| --- | --- | --- | --- |
| 0 | **Coordinator** (you + one main session) | Turns the roadmap into issues, assigns them to lanes, merges PRs, decides priorities | Daily, about 15 min |
| 1 | **Database & Security** | Schema, migrations, RLS, types, the `src/data/` query layer | On demand, when contract requests come in |
| 2 | **Content & Data** | Importer, seed data, vendor/pastime/video/visa content | In parallel, continuously |
| 3 | **Offline Pack** | "Download this yatra before you leave" (Phase 2, highest value) | In parallel |
| 4 | **Admin Editing UI** | Forms for yatras, itinerary days, vendors, rates | In parallel |
| 5 | **Features** | Route map, Telugu UI, visa guide screens, later Phase 3 items | After Waves 1–2 |
| 6 | **QA & Review** | Reviews every PR, runs RLS tests, checks a yatri can't see staff data | Automatic on each PR + nightly |
| 7 | **Docs & Training** | README, docs/, a phone-friendly user guide for coordinators and tour leaders | In parallel, low priority |

Seven agents is the ceiling. Agents 3 and 4 can be one agent if you'd rather
have fewer things to watch.

---

## 3. Lanes: who owns which files

| Agent | Writes to (owns) | Must not touch |
| --- | --- | --- |
| Database & Security | `supabase/migrations/`, `scripts/rls_test.sql`, `scripts/validate_db.sh`, `scripts/check_queries.py`, `scripts/supabase_stub.sql`, `src/types/db.ts`, `src/data/` | `src/pages/`, `src/components/` |
| Content & Data | `scripts/import_content.py`, `supabase/seed/README.md`, `content/` (new: CSV templates and curated lists) | migrations, `src/` |
| Offline Pack | `src/offline/` (new), `src/pages/YatraDetail.tsx` (download button only), `vite.config.ts` (service-worker section only) | `src/data/` (asks Database agent) |
| Admin Editing UI | `src/pages/admin/` (new), `src/components/admin/` (new) | `src/data/` (asks Database agent) |
| Features | `src/pages/<feature>/` and `src/components/<feature>/` (new, one folder per feature) | `src/data/`, other agents' folders |
| QA & Review | Nothing in `src/` — it comments on PRs, and only adds test files under `tests/` (new) | everything else |
| Docs & Training | `docs/`, `README.md` | code |
| Integrator (Coordinator) | Hotspot files from rule 4, `.github/`, `CLAUDE.md`, `.claude/` | — |

If an agent needs a file outside its lane, it stops and opens an issue. It does
not edit the file "just this once".

---

## 4. What each agent works on

### Agent 1: Database & Security
- `translations` table (key: table, row id, column, lang) for Telugu. Build it
  **before** the team enters lots of content, because it's cheaper now.
- Write policies and any RPCs the Admin UI needs (`upsert_itinerary_day`, …).
- `yatra_destinations` backfill support for the route map.
- An offline-pack read model: one RPC, `yatra_pack(slug)`, that returns
  itinerary + hotels + packing list + SOS in one call.
- Visa guide table (`visa_guides`: country, documents, processing days, notes).
- Every migration ships with new assertions in `scripts/rls_test.sql`.

### Agent 2: Content & Data
- **Vendors:** a `content/vendors.csv` template (name, category, city, phone,
  rate, valid till). Pre-fill it with the vendors already named in the notes
  (Himalayan, Heli Yatra, Veena World, RCS, Rao Travels, Jet Wing, Well Nepal).
  A staff member fills in the numbers, and the importer loads them.
- **Videos:** a curated list of expert YouTube videos per yatra, with a title, a
  one-line reason and the yatra slug.
- **Pastimes:** short narrations for the top temples on the most-run yatras.
- **Visa guides:** content for Nepal/Kailash, Sri Lanka, Bhutan and any other
  countries the yatras visit.
- Fix the two unmatched travel windows ("Char Dham Helicopter", "USA").
- **Privacy rule:** personal contact details (devotees, doctors, donors) never
  go into git. They go into Supabase only, as the seed README already requires.

### Agent 3: Offline Pack
- "Download for the trip" button on a yatra page.
- Store the pack in IndexedDB. Show a "Downloaded · updated 3 days ago" badge.
- Works in airplane mode: itinerary, hotel contacts, packing list, SOS.
- Test this by switching the browser to offline.

### Agent 4: Admin Editing UI
- Forms for `yatras`, `itinerary_days`, `vendors` and `vendor_rates`.
- Visible to staff only. RLS remains the real lock.
- Goal: retire the spreadsheets, so nobody has to open the Supabase table editor.

### Agent 5: Features (Wave 2+)
- Route map ("which yatras visit Tirupati").
- Telugu language toggle (needs Agent 1's `translations` table).
- Visa guide screen.
- Phase 3: enquiry capture, per-yatra SOS protocol, tour-leader mode,
  Pushkaram/Kumbh long-range view.

### Agent 6: QA & Review
- Runs `/code-review` and `/security-review` on every PR.
- Logs in as a **yatri** test user and confirms that no pricing, vendors or
  margins leak.
- Nightly: runs the full validation set on `main` and opens an issue if anything
  is red.

### Agent 7: Docs & Training
- A one-page "How to use the app" guide for each role (yatri, tour leader,
  finance, admin).
- Keeps `docs/ROADMAP.md` statuses current as PRs merge.

---

## 5. Order of work (waves)

Within a wave, everything runs in parallel. A wave starts when the items it
depends on have merged.

```
Wave 0 ── Setup (Coordinator, about 1 day)
   │
   ├─ Wave 1 ── in parallel ─────────────────────────────────────────────
   │    Agent 1: translations table, yatra_pack RPC, visa_guides table
   │    Agent 2: vendor/video/visa content templates + data
   │    Agent 3: offline pack UI (starts on existing queries, switches to yatra_pack)
   │    Agent 4: admin forms for yatras + itinerary_days
   │    Agent 7: role guides
   │    Agent 6: reviews everything above
   │
   ├─ Wave 2 ── in parallel ─────────────────────────────────────────────
   │    Agent 4: vendor + rate forms
   │    Agent 5: Telugu toggle, route map, visa screen
   │    Agent 2: Telugu translations of key content
   │
   └─ Wave 3 ── Phase 3 ─────────────────────────────────────────────────
        Enquiry capture → SOS per yatra → Tour-leader mode (needs offline writes)
```

### Wave 0: setup checklist (do this before starting any agent)

1. **`CLAUDE.md` at the repo root.** These are shared rules every agent reads
   automatically: stack, lanes table, the five rules, the done checks, the
   privacy rule.
2. **`.claude/agents/<lane>.md`.** One file per agent, holding its mission, owned
   folders, forbidden folders and its definition of done. Section 6 has a
   template.
3. **GitHub labels:** `lane:db`, `lane:content`, `lane:offline`, `lane:admin`,
   `lane:features`, `lane:docs`, `contract-request`, `blocked`, `needs-human`.
4. **GitHub issues:** one per task in section 4, labelled by lane and wave.
   Each issue holds the instructions for its task, so an agent can start from
   the issue alone.
5. **CI workflow** `.github/workflows/check.yml`: typecheck, build, DB
   validation, query check.
6. **Branch protection on `main`:** require a PR and passing CI.
7. **Cloud environment:** network access for npm and pip, and a setup script
   that runs `npm ci` and installs Postgres for `validate_db.sh`.

---

## 6. Agent instruction template

Every `.claude/agents/<lane>.md` follows this shape:

```markdown
---
name: offline-pack
description: Builds the offline "download this yatra" feature.
---
You are the Offline Pack agent for the Yatra Knowledge Base.

## Mission
<one paragraph>

## You own (may write)
- src/offline/
- ...

## You must not edit
- src/data/ — open an issue labelled contract-request instead
- src/routes/AppRoutes.tsx, package.json — list the change in your PR description

## Workflow
1. Read CLAUDE.md, docs/ARCHITECTURE.md and your issue.
2. Work on branch agent/offline/<task>.
3. Before opening the PR run: npm run typecheck && npm run build
4. Open a PR that links the issue and lists:
   what changed, how you tested it, any hotspot edits needed, open questions.
5. If blocked, label the issue `blocked`, say what you need, and move to the
   next task in your lane.

## Definition of done
- Checks green, PR open, issue linked, no files outside your lane.
```

---

## 7. How the agents talk to each other

Agents don't message each other directly. Everything goes through GitHub, so
you can always see the state of the work.

| Situation | What the agent does |
| --- | --- |
| Needs a new column, table or query | Opens an issue labelled `contract-request` + `lane:db`, then continues with mock data behind a clearly marked `TODO(contract)` |
| Needs a route, nav entry or dependency | Lists it under **Hotspot edits** in the PR description |
| Blocked on a human decision | Labels the issue `needs-human` and asks one clear question |
| Finishes a task | Opens the PR and picks the next open issue in its lane |

---

## 8. Your daily routine (about 15 minutes)

1. Open GitHub issues filtered by `needs-human` and answer them.
2. Open PRs with green CI and a QA-agent approval. Skim each and merge it.
   Apply hotspot edits while merging, or ask the Coordinator session to do it.
3. Look at `contract-request` issues and make sure the Database agent is working
   on them.
4. Once a week: reorder priorities in the issue list and update the roadmap.

Everything else runs without you.

---

## 9. How to actually launch them

| Mechanism | Use it for |
| --- | --- |
| **One cloud session per agent** (claude.ai/code, this repo, its own branch). Paste: "You are the `<lane>` agent. Read `.claude/agents/<lane>.md` and work on issue #N." | Agents 1–5 and 7, the main build work |
| **PR subscription** in each session | Lets an agent fix its own CI failures and respond to review comments automatically |
| **Routines (scheduled triggers)** | Nightly QA run on `main`, weekly roadmap/status update by the Docs agent |
| **Subagents from the Coordinator session** | Small one-off jobs (a quick search, a single review) without opening a new session |

Start with **3 agents in parallel** (Database, Offline Pack, Content) for the
first week. Add the rest once the lane rules have proven themselves.

---

## 10. Decisions only you can make

Answer these before Wave 1 starts. Each one unblocks an agent.

1. **Priority order:** is Offline Pack first, or Admin Editing UI?
2. **Vendor data:** who on the team fills in phone numbers and rates in
   `content/vendors.csv`?
3. **Telugu:** do you want it in this cycle (Wave 2), or later?
4. **Who merges:** only you, or a second trusted staff member as well?
5. **Supabase:** do agents get a separate staging project, so they never test
   against the live data your ~100 users rely on? (Strongly recommended.)
