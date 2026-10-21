"""Small, dependency-free guards for collaborative agent changes."""
PROTECTED_ACTIONS = frozenset({"send_outreach", "submit_application", "purchase", "transfer_money"})


def may_execute(action: str, approved_actions: set[str]) -> bool:
    """Only execute protected actions if that individual action was approved."""
    return action not in PROTECTED_ACTIONS or action in approved_actions


def check_revision(expected: str, actual: str) -> None:
    """Reject edits based on stale shared state."""
    if expected != actual:
        raise ValueError("Revision conflict: reload and reconcile before writing")
