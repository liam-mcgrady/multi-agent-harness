# Option A — ChatGPT-mediated Drive ⇄ GitHub coordination

**Status:** active operating procedure for ChatGPT-assisted sessions, not a continuously running two-way synchronization service.

## Sources of truth

- Google Drive HARNESS.md and its companion files are authoritative for agent roles, schedule, academic and business context.
- Google Doc "Agent Journal" is the append-only cross-agent decision / handoff log; routine work within an agent's lane does not require a Journal entry.
- GitHub holds versioned **code, schemas, tests, non-sensitive implementation decisions, and change proposals**. No broad mirroring of confidential Drive content.
- Muse coordinates and reconciles calendar/shared planning; ChatGPT implements mathematical reasoning, ML research and experiments, engineering, and technical documentation as requested. Other agents retain their stated lanes.
- Your Apple/iCloud calendar is the scheduling source of truth; a Google Calendar read view is not an authorized write destination.

## ChatGPT-mediated synchronization sequence

1. **Read latest:** fetch live HARNESS.md and the recent Agent Journal entries before cross-agent work. Read domain files strictly as necessary.
2. **Inspect destination:** read GitHub branch, file content and blob SHA before proposing changes. Never assume the local copy is current.
3. **Classify:** distinguish routine in-lane work from cross-agent decisions, write proposals, sensitive records, and protected external actions.
4. **Propose:** state files to change and exact intended behavior. For shared-state edits, require fresh revision/etag and a reviewed change. Never blindly replace another agent's work.
5. **Apply the relevant atomic edit:**
   - GitHub: update with existing content SHA, preferably in a topic branch and pull request.
   - Google Docs: use `requiredRevisionId` and an explicit tab ID.
   - Raw Drive Markdown: do not force content replacement without an adapter with version preconditions and readback.
   - Google Sheets: use a purpose-built cell/range update and re-read the affected rows.
6. **Verify:** read back the changed file or changed range, record revision/commit identifier and relevant summary.
7. **Handoff:** add a concise dated Journal entry for a decision, cross-agent handoff, or open loop; skip routine in-lane narration per current HARNESS rule 7.
8. **Resolve conflicts:** halt, re-read live state, and propose a merge; don't overwrite a newer agent's change.

## Permission and confidentiality model

- A rule granting agents conceptual rights **does not grant OAuth/API permissions**; each agent's connector controls its actual capabilities.
- Never commit OAuth credentials, client secrets, private academic notes, PLUNJ sales records, financial data, or personal information into GitHub.
- Per-item approvals remain mandatory for submitting applications, sending outreach, purchases or transfers. Drafting and internal updates do not constitute approval.
- The existing GitHub Actions Drive sync remains opt-in and inactive unless `DRIVE_SYNC_ENABLED=true` is explicitly configured.

## Triggering

- On-demand: invoke ChatGPT for a specific update or use a scheduled ChatGPT task to inspect connected context when supported.
- Daily review is already scheduled within ChatGPT. It identifies changed state but does not automatically write back to Drive or GitHub.
- Do not describe this workflow as real-time or continuous.

## First acceptance test

1. Read HARNESS.md and the latest Agent Journal.
2. Read the current GitHub proposal.
3. Commit the non-sensitive mediation protocol on a GitHub branch using the latest SHA.
4. Log the resulting cross-agent decision once in the Agent Journal with revision guard.
5. Read back to confirm both sides show the decision.
