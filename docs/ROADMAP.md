# Roadmap

## Implemented prototype

- Allowlisted Drive metadata reader and snapshot comparison.
- Tab-specific native Docs append with a required revision.
- Fake-transport tests and offline conflict demo.
- Synthetic configuration and public-tree privacy checks.

## Remaining engineering

- Authenticated, proposal-specific approval records.
- Runtime schema validation and private audit persistence.
- Idempotency and ambiguous-result reconciliation.
- Real-API tests against disposable documents.
- Multi-agent connector capability verification per deployment.

## Publication gate

Current-tree sanitization does not erase historical disclosures. Review all branches, tags, PR diffs, commit metadata, Actions logs, and artifacts before calling a repository sanitized. History replacement and host-side removal of retained references are separate operations.
