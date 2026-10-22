# Public/private boundary

| Safe public material | Private deployment material |
| --- | --- |
| Generic code, schemas, tests | Tokens, keys, authentication state |
| Synthetic agent registry | Actual agent assignments and permissions |
| Dummy document IDs | Real document IDs, titles, revisions, links |
| Offline demo output | Journals, schedules, personal or business records |
| Architecture and limitations | Live metadata snapshots and audit records |

Use a separate private deployment repository or protected local directory. Files ignored by Git can still be force-added; ignore rules are convenience, not access control. The Python adapter uses environment variables, not the example JSON, for runtime IDs and credentials.

`python scripts/check_public.py` checks tracked working-tree content for selected credential patterns, Google document links, plausible Drive IDs, and forbidden local deployment paths. It reports filenames and rule labels without printing matched values. This heuristic is not a general secret detector or proof that prose contains no personal information. Review staged changes manually too.

The public demo is entirely synthetic and network-free. Live metadata is sensitive even when document bodies are excluded. Avoid public Actions for real deployment metadata; use a controlled environment with private logs and artifact retention.

Deleting a value from HEAD does not remove it from history, PR references, forks, caches, or existing clones. For an actual credential exposure, revoke the credential first. Document identifiers do not independently grant document access, but should still be removed from public examples.
