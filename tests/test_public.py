import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(ROOT / 'examples'))
from check_public import violations
from demo import run_demo


class PublicTests(unittest.TestCase):
    def test_synthetic_fixture_allowed(self):
        self.assertEqual(violations('config/example.json', 'DEMO_JOURNAL_ID'), [])

    def test_document_identifier_rejected(self):
        self.assertIn('plausible-drive-id', violations('config/example.json', '1' + 'a' * 30))

    def test_token_rejected_without_echo(self):
        self.assertEqual(violations('example.txt', 'ghp_' + 'a' * 36), ['github-token'])

    def test_private_path_rejected(self):
        self.assertIn('private-deployment-path', violations('private/settings.json', '{}'))

    def test_demo_does_not_duplicate_write(self):
        self.assertEqual(run_demo().writes, 1)
