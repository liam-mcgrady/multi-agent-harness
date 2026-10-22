# Connector-mediated coordination

This is an on-demand operating procedure for a host with authorized document and repository connectors. It creates no scheduled task and provides no continuous synchronization.

1. Read the authoritative private policy and recent relevant handoffs.
2. Inspect the destination and capture its current revision or blob SHA.
3. Establish authorization for the exact proposed change and destination.
4. Apply a scoped edit using a server-enforced revision precondition.
5. Read back once, verify the result, and record a concise private handoff.
6. On conflict or uncertain outcome, inspect current state before retrying.

GitHub file edits use the existing blob SHA. Native Google Docs appends use `requiredRevisionId` and an explicit tab ID. A Sheets range readback does not provide atomic compare-and-swap. Raw Markdown writes require a separate adapter with atomic preconditions.

Private policy defines roles and calendar ownership; this public project does not prescribe a personal deployment. Conceptual permission does not grant connector access. External actions remain subject to the host's own authorization controls.

Existing host connections do not expose their credentials to standalone Python programs. The optional API adapter has separate credential requirements. Keep private context out of public commits, issues, pull requests, logs, and artifacts.
