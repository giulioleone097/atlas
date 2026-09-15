"""Identify Atlas hooks before merging a shared host configuration."""

import json
from pathlib import Path
import shlex


def is_atlas_hook(command: str, root: str) -> bool:
    if not isinstance(command, str):
        return False
    try:
        args = shlex.split(command)
    except (ValueError, TypeError):
        return False
    if len(args) != 2 or args[0] not in ("sh", "/bin/sh"):
        return False
    script = Path(args[1])
    if script.name not in ("core-context.sh", "guard.sh") or script.parent.name != "scripts":
        return False
    owner = script.parent.parent
    if owner.resolve() == Path(root).resolve():
        return True
    # A previous Atlas checkout/cache can own the old hook. Identical script
    # names in another plugin do not establish ownership.
    for name in (".claude-plugin", ".codex-plugin"):
        try:
            manifest = json.loads((owner / name / "plugin.json").read_text())
        except (OSError, ValueError):
            continue
        if isinstance(manifest, dict) and manifest.get("name") == "atlas":
            return True
    return False
