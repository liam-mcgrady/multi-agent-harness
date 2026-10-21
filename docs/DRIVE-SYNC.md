# Drive synchronization and guarded editing (phase 1)

**Current deployment choice: Option A (ChatGPT-mediated).** See [CHATGPT-MEDIATED-SYNC.md](CHATGPT-MEDIATED-SYNC.md). The Python Google API connector and GitHub Actions workflow below are optional future infrastructure and **are not required for Option A**. No new Google Cloud OAuth credentials are needed for ChatGPT's existing connected Drive and GitHub workflows. These connections do not supply credentials to standalone Python programs or GitHub Actions.


**Authority:** Live Google Drive files remain source of truth. The GitHub repository stores code and optional metadata snapshots, not the user’s private Drive content.

## Setup

1. Enable Drive API and Docs API for an appropriately authorized Google Cloud OAuth client.
2. Provision a least-privilege OAuth access token outside the repository. For local use, set GOOGLE_ACCESS_TOKEN in your shell. Never store tokens in files or Git history.
3. Set DRIVE_ALLOWLIST_IDS to explicitly approved file IDs and run `python src/drive_sync.py`. Example IDs are in config/drive-files.example.json.
4. The resulting drive-snapshot.json contains names, IDs, versions, timestamps and document revision IDs, **not document text**. Compare it with a prior snapshot to detect additions, removals, and changes.
5. For writing, construct an AppendProposal from a specific human-approved change. Capture the current Google Docs revision, supply an explicit writable file allowlist and tab ID (e.g., the current Agent Journal tab ID), and call append_document. Its Google Docs requiredRevisionId prevents overwrites when the document changed.
6. Raw Markdown files, Sheets, deletion, global edits, cross-file transactions and unattended writebacks are **not implemented**.

## Security and limitations

- This is a version-aware *metadata sync*, not a live two-way mirror. Only configured file IDs are checked.
- OAuth tokens obtained through ChatGPT connectors are not automatically accessible to GitHub Actions or a Python process. Configure credentials separately if automating.
- Drive file `version` is not interchangeable with Docs `revisionId`.
- Document revision IDs need fresh reads. Avoid storing them as durable edit locks for long periods.
- Guarded append explicitly requires approval and a writable allowlist; no automatic write is invoked by scheduled tasks.
- `endOfSegmentLocation` writes to the document body’s end; complex tabbed Docs require tab-specific targeting before this is enabled for those documents.
- Read-only sync is safe to run unattended; edits require a separate reviewed application workflow.
- Never upload private academic, customer, financial, or personal document bodies as CI logs/artifacts.
