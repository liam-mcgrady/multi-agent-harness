import io
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from drive_sync import metadata_snapshot, diff_snapshots, DriveError
from guarded_docs import AppendProposal, append_document, validate_proposal


class Response(io.BytesIO):
    def __enter__(self):
        return self
    def __exit__(self, *args):
        self.close()


class FakeGoogle:
    def __init__(self, rev="rev-a"):
        self.rev = rev
        self.calls = []
    def __call__(self, request):
        self.calls.append(request)
        url = request.full_url
        if "/drive/v3/files/" in url:
            obj = {"id": "doc1", "name": "Agent Journal", "mimeType":
                   "application/vnd.google-apps.document", "version": "9"}
        elif request.get_method() == "POST":
            obj = {"documentId": "doc1", "writeControl": {"requiredRevisionId": self.rev}}
        else:
            obj = {"documentId": "doc1", "revisionId": self.rev}
        return Response(json.dumps(obj).encode())


class SyncTests(unittest.TestCase):
    def test_snapshot_has_revision_and_no_body(self):
        fake = FakeGoogle()
        snap = metadata_snapshot(["doc1"], "example-token", fake)
        self.assertEqual(snap["files"][0]["docs_revision"], "rev-a")
        self.assertNotIn("content", json.dumps(snap))
        self.assertEqual(len(snap["fingerprint"]), 64)
        self.assertTrue(all(call.get_method() == "GET" for call in fake.calls))

    def test_diff(self):
        old = {"files": [{"id": "a", "version": "1"}]}
        new = {"files": [{"id": "a", "version": "2"}, {"id": "b", "version": "1"}]}
        self.assertEqual(diff_snapshots(old, new), {"added": ["b"], "removed": [], "changed": ["a"]})

    def test_requires_approval(self):
        with self.assertRaises(PermissionError):
            validate_proposal(AppendProposal("doc1", "rev-a", "chatgpt", "hello"), {"doc1"})

    def test_no_raw_file_or_unknown_target(self):
        with self.assertRaises(PermissionError):
            validate_proposal(AppendProposal("other", "rev-a", "chatgpt", "hello", True), {"doc1"})

    def test_stale_revision_does_not_write(self):
        fake = FakeGoogle(rev="rev-b")
        with self.assertRaises(DriveError):
            append_document(AppendProposal("doc1", "rev-a", "chatgpt", "hello", True), "token", {"doc1"}, fake)
        self.assertTrue(all(call.get_method() == "GET" for call in fake.calls))

    def test_approved_append_uses_atomic_revision_guard(self):
        fake = FakeGoogle()
        append_document(AppendProposal("doc1", "rev-a", "chatgpt", "hello", True), "token", {"doc1"}, fake)
        posts = [x for x in fake.calls if x.get_method() == "POST"]
        self.assertEqual(len(posts), 1)
        payload = json.loads(posts[0].data)
        self.assertEqual(payload["writeControl"]["requiredRevisionId"], "rev-a")

    def test_empty_allowlist_rejected(self):
        with self.assertRaises(ValueError):
            metadata_snapshot([], "token")


if __name__ == "__main__":
    unittest.main()
