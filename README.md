# Multi-Agent Harness

Private, GitHub-backed coordination for Muse, Claude, Gemini, ChatGPT, and GitHub Copilot.

## Principles

- Keep the existing Google Drive harness authoritative until synchronization is implemented and tested.
- Allow every agent to read and propose edits, subject to actual connector permissions.
- Log changes with agent identity, timestamp, target, and base revision.
- Use branches and reviewed pull requests for protected or conflicting changes.
- Never submit applications, send outreach, make purchases, or transfer funds without per-action human approval.
- Never commit credentials or private academic, sales, or personal records.

## Roadmap

1. Implement shared agent registry and versioned event schema.
2. Add tests and GitHub Actions validation.
3. Implement a read-only Google Drive synchronization adapter.
4. Implement guarded edits, conflict handling, and a human approval queue.
5. Integrate Codex and GitHub Copilot through scoped issues and pull requests.

This repository is an engineering scaffold, not a replacement for the live Drive context.