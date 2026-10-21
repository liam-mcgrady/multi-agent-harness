import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from governance import may_execute, check_revision


class GovernanceTests(unittest.TestCase):
    def test_protected_action(self):
        self.assertFalse(may_execute("send_outreach", set()))
        self.assertTrue(may_execute("send_outreach", {"send_outreach"}))

    def test_unprotected_action(self):
        self.assertTrue(may_execute("draft_research", set()))

    def test_revision_conflict(self):
        with self.assertRaises(ValueError):
            check_revision("v1", "v2")

    def test_matching_revision(self):
        check_revision("v1", "v1")


if __name__ == "__main__":
    unittest.main()
