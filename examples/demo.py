"""Synthetic, network-free exercise of the real guarded append adapter."""
import io
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from drive_sync import DriveError
from guarded_docs import AppendProposal, append_document


class MemoryDocs:
    def __init__(self):
        self.revision = 'demo-rev-1'
        self.text = ''
        self.writes = 0

    def __call__(self, request):
        if '/drive/v3/files/' in request.full_url:
            result = {'id': 'demo-doc', 'name': 'Synthetic journal',
                      'mimeType': 'application/vnd.google-apps.document'}
        elif request.get_method() == 'POST':
            payload = json.loads(request.data)
            if payload['writeControl']['requiredRevisionId'] != self.revision:
                raise DriveError('Server rejected stale revision')
            self.text += payload['requests'][0]['insertText']['text']
            self.writes += 1
            self.revision = f'demo-rev-{self.writes + 1}'
            result = {'documentId': 'demo-doc', 'writeControl': {'requiredRevisionId': self.revision}}
        else:
            result = {'documentId': 'demo-doc', 'revisionId': self.revision}
        return io.BytesIO(json.dumps(result).encode())


def run_demo():
    server = MemoryDocs()
    proposal = AppendProposal('demo-doc', server.revision, 'builder-demo',
                              'Synthetic task completed.\n', True, tab_id='demo-tab')
    append_document(proposal, 'synthetic-token', {'demo-doc'}, server)
    assert server.text == proposal.text and server.writes == 1
    print('APPROVED: one synthetic journal append verified')
    try:
        append_document(proposal, 'synthetic-token', {'demo-doc'}, server)
    except DriveError:
        print('STALE: old proposal rejected; no second write')
    else:
        raise AssertionError('Stale proposal was accepted')
    unapproved = AppendProposal('demo-doc', server.revision, 'builder-demo',
                                'Should not be written', tab_id='demo-tab')
    try:
        append_document(unapproved, 'synthetic-token', {'demo-doc'}, server)
    except PermissionError:
        print('UNAPPROVED: proposal rejected; no second write')
    else:
        raise AssertionError('Unapproved proposal was accepted')
    assert server.writes == 1
    return server


if __name__ == '__main__':
    run_demo()
