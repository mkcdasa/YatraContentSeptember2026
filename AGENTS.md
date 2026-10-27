# AGENTS.md

<!-- handoff:learnings:begin -->
## Session Learnings (auto-updated by handoff)

### Implicit Rules
- Build: python3 scripts/hr_tracker/build_hr_tracker.py <scratchpad-out-dir>; reads <out>/links.json for sheet/clickup/doc links
- Git: branch claude/fervent-edison-meesy5; commits end with Co-Authored-By Claude Fable 5.1 line and Claude-Session URL; no model IDs inside repo files
- ClickUp: HR Department space 90165770409, folder 90167634196, list 1300380000011033 'MKCD Follow-up Action Items (WhatsApp) - Due 10 Nov 2026'; GN user id 100909505; tag mkcd-followup; due_date 1794292200000 with due_date_time false
- Claude Docs: Action Items doc project 4e8d5dcc-105a-404d-8be9-2f044690766b node 1d9becf0-3cbf; HR R&R doc project c20416db-0d3b-4322-9f36-2e507baafc4e node 3b03de69-b393 (rev 2 after section 9A); GN living doc project 861b8446-f771-457d-b538-ca8cb1156337; RP living doc project 668ecc06-2af2-4b8b-a9b7-3d9c0134abd6
- Google Sheet tracker id 1fzmkRrOWSxG5Y744AHJ7p-IPqXVCxwd0yw_SvUi-lzo, single tab 'Untitled', 13 columns A-M, header row 1, B8 is row 17
- Owners abbreviations: RP, GN, BOTH, MKCD; statuses COMPLETED/PENDING/PARTIAL/VERIFY/RECURRING; priorities urgent/high/normal/low
- Permission prompts: cloud session mode only changeable by user via app mode dropdown (Auto); never suggest CLI flags

### Key Decisions
- Decision: one data file scripts/hr_tracker/hr_tasks_data.py drives xlsx/md/ClickUp JSON via build_hr_tracker.py — Reason: single source of truth, regenerate all outputs after any edit
- Decision: sweep items go in category I, 25-Oct payroll decisions in category J; existing rows get CROSS_REFS evidence notes instead of duplicate rows — Reason: keep original WhatsApp IDs stable for ClickUp task names
- Decision: J12 (Gnaneshwar termination discussion) in Sheet only, clickup=False — Reason: ClickUp list is assigned to Gnaneshwar himself
- Decision: update existing Google Sheet in place via Google_Sheets update_values, never create new Drive files — Reason: every Drive create_file triggers a permission prompt the user explicitly rejected
- Decision: R&R additions appended to existing Claude Doc HR — Dept R&R (Oct 2026) as section 9A — Reason: user already had that living doc; corrects earlier claim that none existed
- Decision: ClickUp tasks created via task.create_many in batches of ~13-17 — Reason: 50+ task payload exceeded size limit

<!-- handoff:learnings:end -->
