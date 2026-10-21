# Readiness and remaining work

Verified 2026-10-21. Option A is connector-mediated, on-demand coordination. Separate Google API credentials are not required for this operating mode.

## Verified

- [x] Repository and draft PR #1 exist.
- [x] CI passed at commit 06b84d465b7190e5239011d7f85ad569044e8310 (run 39526804592); this is not a claim about later commits.
- [x] Live governance and recent journal entries inspected.
- [x] Registry now defers role definitions to the live authoritative harness.
- [x] Optional metadata reader and revision-guarded Docs append adapter exist, with fake-transport unit tests.

## Activation gates

- [ ] Set repository visibility to private. It was public at inspection, contrary to the intended setup. Connected tools do not expose visibility updates.
- [ ] Configure and verify main-branch protection and required CI. The rulesets endpoint returned an empty list; legacy branch protection was not verified.
- [ ] Complete review and merge PR #1 after checks pass on its final head.
- [ ] Verify each external agent's actual connector read/write capability in that agent's own session. Policy statements alone are not evidence of access.
- [ ] Validate any scheduled review against the actual task system before relying on it.

## Deliberate limits

- Drive remains authoritative; no private document mirroring to GitHub.
- Option A requires an active agent session; it is not continuous synchronization.
- Raw Markdown replacement remains unsupported without atomic version preconditions and readback.
- Sheets range readback detects errors but does not provide atomic compare-and-swap.
- The optional Google-auth workflow is gated by DRIVE_SYNC_ENABLED. Do not enable it for Option A; its credentials and real-API validation are deferred.
- Unit tests do not prove live Google API permissions or all agents' integration.

## Session acceptance check

Read live source and destination, apply a SHA-guarded GitHub update, append one revision-guarded journal handoff, and read both back. Record results in the journal; do not publish private source contents here.
