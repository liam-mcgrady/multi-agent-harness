"""Heuristic public-tree checks. Never prints matched sensitive values."""
import re
import subprocess
from pathlib import Path

RULES = {
    'private-key': re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    'github-token': re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})\b'),
    'google-access-token': re.compile(r'\bya29\.[A-Za-z0-9_-]{20,}'),
    'google-api-key': re.compile(r'\bAIza[A-Za-z0-9_-]{30,}'),
    'google-document-link': re.compile(r'https://(?:docs|drive)\.google\.com/(?:document|spreadsheets|presentation|file)/d/[A-Za-z0-9_-]{20,}'),
    'plausible-drive-id': re.compile(r'(?<![A-Za-z0-9_-])1[A-Za-z0-9_-]{24,}(?![A-Za-z0-9_-])'),
}


def violations(path, text):
    findings = [name for name, pattern in RULES.items() if pattern.search(text)]
    p = Path(path)
    if any(x in {'private', 'secrets', 'local'} for x in p.parts) or p.name.startswith('.env') or p.name.endswith(('.local.json', '.pem', '.key')) or 'drive-snapshot' in p.name:
        findings.append('private-deployment-path')
    return findings


def main():
    root = Path(__file__).resolve().parents[1]
    paths = subprocess.check_output(['git', 'ls-files', '-z'], cwd=root).decode().split('\0')
    failed = False
    for name in filter(None, paths):
        path = root / name
        if not path.is_file():
            continue
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            print(f'{name}: binary requires manual review')
            failed = True
            continue
        for label in violations(name, text):
            print(f'{name}: {label}')
            failed = True
    if not failed:
        print('Public-tree heuristic checks passed (manual review still required).')
    return int(failed)


if __name__ == '__main__':
    raise SystemExit(main())
