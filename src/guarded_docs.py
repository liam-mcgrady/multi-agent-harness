"""Guarded Google Docs append workflow.

Only native Google Docs are writable here. Raw .md Drive files are deliberately
excluded: a separate atomic compare-and-swap adapter is required for them.
"""
import os
import urllib.parse
from dataclasses import dataclass
from drive_sync import DOCS_API, DriveError, docs_revision, drive_metadata, http_json

DOC_MIME = "application/vnd.google-apps.document"
PROTECTED_ACTIONS = frozenset(("send_outreach", "submit_application", "purchase", "transfer_money"))


@dataclass(frozen=True)
class AppendProposal:
    file_id: str
    expected_revision: str
    agent: str
    text: str
    approval: bool = False
    action: str = "append_journal"
    tab_id: str = ""


def validate_proposal(proposal, allowlist):
    if not proposal.file_id or proposal.file_id not in allowlist:
        raise PermissionError("Destination not in explicit writable allowlist")
    if not proposal.agent.strip() or not proposal.text.strip():
        raise ValueError("Agent and non-empty text are required")
    if not proposal.tab_id.strip():
        raise ValueError("An explicit Google Docs tab ID is required")
    if not proposal.expected_revision:
        raise ValueError("Expected document revision is required")
    if len(proposal.text) > 5000:
        raise ValueError("Append proposal too long")
    if proposal.action in PROTECTED_ACTIONS:
        raise PermissionError("Protected external actions are not supported by this adapter")
    if not proposal.approval:
        raise PermissionError("An explicitly approved append proposal is required")


def append_document(proposal, token, allowlist, opener=None):
    """Single guarded append; Google rejects it if revision changes concurrently."""
    validate_proposal(proposal, allowlist)
    meta = drive_metadata(proposal.file_id, token, opener=opener)
    if meta["mimeType"] != DOC_MIME:
        raise DriveError("Only native Google Docs can be appended; raw markdown unchanged")
    actual = docs_revision(proposal.file_id, token, opener=opener)
    if actual != proposal.expected_revision:
        raise DriveError("Stale revision: reload and resolve conflict before retry")
    endpoint = DOCS_API + "/documents/" + urllib.parse.quote(proposal.file_id, safe="") + ":batchUpdate"
    result = http_json(endpoint, token, method="POST", body={
        "requests": [{"insertText": {"endOfSegmentLocation": {"tabId": proposal.tab_id}, "text": proposal.text}}],
        "writeControl": {"requiredRevisionId": proposal.expected_revision},
    }, opener=opener)
    if not result.get("writeControl") and not result.get("documentId"):
        raise DriveError("Write result ambiguous; verify document before retry")
    return result


def main():
    raise SystemExit("No unattended writes. Supply an explicitly approved AppendProposal via your application.")


if __name__ == "__main__":
    main()
