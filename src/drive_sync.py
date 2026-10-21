"""Version-aware Google Drive metadata synchronization. Standard library only.

Only metadata is exported; no document contents or tokens are persisted.
Read-only: never calls Drive mutations or writes to the source files.
"""
import hashlib
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

DRIVE_API = "https://www.googleapis.com/drive/v3"
DOCS_API = "https://docs.googleapis.com/v1"


class DriveError(RuntimeError):
    pass


def http_json(url, token, method="GET", body=None, opener=None):
    """Make a JSON API request with OAuth bearer token; injectable for tests."""
    if not token:
        raise DriveError("Missing GOOGLE_ACCESS_TOKEN")
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": "Bearer " + token,
            "Accept": "application/json",
            **({"Content-Type": "application/json"} if data is not None else {}),
        },
        method=method,
    )
    try:
        response = (opener or urllib.request.urlopen)(req)
        with response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        raise DriveError("Google API returned HTTP " + str(exc.code)) from exc


def drive_metadata(file_id, token, opener=None):
    query = urllib.parse.urlencode({
        "fields": "id,name,mimeType,modifiedTime,version,md5Checksum,parents,webViewLink",
        "supportsAllDrives": "true",
    })
    url = DRIVE_API + "/files/" + urllib.parse.quote(file_id, safe="") + "?" + query
    obj = http_json(url, token, opener=opener)
    required = ("id", "name", "mimeType")
    if any(key not in obj for key in required):
        raise DriveError("Incomplete Drive file metadata")
    return obj


def docs_revision(file_id, token, opener=None):
    query = urllib.parse.urlencode({"fields": "documentId,revisionId"})
    url = DOCS_API + "/documents/" + urllib.parse.quote(file_id, safe="") + "?" + query
    obj = http_json(url, token, opener=opener)
    if not obj.get("revisionId"):
        raise DriveError("Docs revision unavailable; cannot safely write")
    return obj["revisionId"]


def metadata_snapshot(files, token, opener=None):
    """Caller supplies explicitly allowlisted IDs, not Drive-wide discovery."""
    if not files or len(files) != len(set(files)):
        raise ValueError("Supply one or more unique allowed file IDs")
    snapshots = []
    for file_id in sorted(files):
        item = drive_metadata(file_id, token, opener=opener)
        entry = {key: item[key] for key in (
            "id", "name", "mimeType", "modifiedTime", "version",
            "md5Checksum", "webViewLink",
        ) if key in item}
        # Docs API revision IDs are distinct from Drive file versions.
        if entry["mimeType"] == "application/vnd.google-apps.document":
            entry["docs_revision"] = docs_revision(file_id, token, opener=opener)
        snapshots.append(entry)
    digest = hashlib.sha256(json.dumps(snapshots, sort_keys=True).encode()).hexdigest()
    return {"schema_version": 1, "fingerprint": digest, "files": snapshots}


def diff_snapshots(previous, current):
    before = {x["id"]: x for x in previous.get("files", [])}
    after = {x["id"]: x for x in current.get("files", [])}
    return {
        "added": sorted(set(after) - set(before)),
        "removed": sorted(set(before) - set(after)),
        "changed": sorted(k for k in set(before) & set(after) if before[k] != after[k]),
    }


def main():
    token = os.environ.get("GOOGLE_ACCESS_TOKEN")
    ids = [x.strip() for x in os.environ.get("DRIVE_ALLOWLIST_IDS", "").split(",") if x.strip()]
    current = metadata_snapshot(ids, token)
    path = Path(os.environ.get("SYNC_SNAPSHOT_PATH", "drive-snapshot.json"))
    if path.exists():
        print(json.dumps(diff_snapshots(json.loads(path.read_text()), current), indent=2))
    else:
        print(json.dumps({"initial": True, "file_count": len(ids)}, indent=2))
    path.write_text(json.dumps(current, indent=2) + "\n")


if __name__ == "__main__":
    main()
