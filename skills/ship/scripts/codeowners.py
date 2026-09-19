#!/usr/bin/env python3
"""Discover CODEOWNERS at a Git revision; does not resolve owners or approvals."""
import argparse
import json
import subprocess

# ceiling: native GitHub/GitLab locations; add a forge after verifying its policy semantics.
LOCATIONS = {
    "github": (".github/CODEOWNERS", "CODEOWNERS", "docs/CODEOWNERS"),
    "gitlab": ("CODEOWNERS", "docs/CODEOWNERS", ".gitlab/CODEOWNERS"),
}


def git(repo, *args):
    return subprocess.run(
        ["git", "-C", repo, *args], check=True, capture_output=True, text=True
    ).stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-C", "--repo", default=".")
    parser.add_argument("--forge", choices=LOCATIONS, required=True)
    parser.add_argument("--ref", required=True, help="Governing target-policy revision")
    parser.add_argument("--show", action="store_true", help="Include selected raw policy text")
    args = parser.parse_args()
    try:
        revision = git(args.repo, "rev-parse", "--verify", "--end-of-options", args.ref + "^{commit}").strip()
        entries = {}
        for row in git(args.repo, "ls-tree", "-z", revision, "--", *LOCATIONS[args.forge]).split("\0"):
            if row:
                metadata, path = row.split("\t", 1)
                mode, kind, oid = metadata.split()
                entries[path] = (mode, kind, oid)
        present = [path for path in LOCATIONS[args.forge] if path in entries]
        result = {"forge": args.forge, "policy_revision": revision,
                  "checked_locations": LOCATIONS[args.forge], "status": "absent",
                  "selected_path": None, "ownership_resolved": False}
        if present:
            selected = present[0]
            mode, kind, oid = entries[selected]
            result.update(selected_path=selected, ignored_locations=present[1:], blob=oid)
            if kind != "blob" or mode not in ("100644", "100755"):
                result.update(status="unresolved", reason="Selected policy is not a regular Git file")
            else:
                result["status"] = "found"
                if args.show:
                    result["content"] = git(args.repo, "show", revision + ":" + selected)
        print(json.dumps(result, ensure_ascii=False))
        return 0 if result["status"] != "unresolved" else 1
    except (subprocess.CalledProcessError, OSError, UnicodeError) as error:
        message = error.stderr.strip() if isinstance(error, subprocess.CalledProcessError) else str(error)
        print(json.dumps({"status": "unavailable", "error": message}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
