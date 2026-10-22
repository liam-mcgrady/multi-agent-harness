# Governance design

This is a reusable design proposal, not an assertion about any live deployment.

- Read current shared state before proposing a change.
- Bind each write to a destination, actor, purpose, and base revision.
- Reject stale writes; reconcile conflicting changes explicitly.
- Keep approval provenance and deployment-specific role assignments private.
- Use reviewed pull requests for code changes.
- Treat connector permissions as independently verified capabilities.
- Let the deployment's coordinator resolve cross-agent conflicts.

The current helper functions illustrate checks, but do not authenticate callers or enforce complete end-to-end policy. Never expose them directly as a trusted authorization boundary.
