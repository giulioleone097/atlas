#!/bin/sh
# Global native Antigravity plugin; keep source-relative skill references intact.
set -eu
ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
exec python3 - "$ROOT" "$HOME/.gemini/config/plugins/atlas" <<'PY'
import json
from pathlib import Path
import shutil
import sys
root, destination = map(Path, sys.argv[1:])
if destination.is_symlink():
    raise SystemExit('Refusing to replace a symlinked plugin directory')
for name in ('skills', 'core', 'agents', 'scripts', 'AGENTS.md', 'README.md', 'LICENSE', 'plugin.json', 'rules', 'rules/atlas-core.md'):
    if (destination / name).is_symlink():
        raise SystemExit('Refusing symlinked plugin component: ' + name)
if destination.exists():
    manifest = destination / 'plugin.json'
    if not manifest.is_file() or json.loads(manifest.read_text()).get('name') != 'atlas':
        raise SystemExit('Destination is not an Atlas plugin')
destination.mkdir(parents=True, exist_ok=True)
for name in ('skills', 'core', 'scripts'):
    target = destination / name
    if target.is_symlink():
        raise SystemExit('Refusing symlinked plugin component: ' + name)
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(root / name, target, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
# Keep the model registry as reference data, without exposing unsupported agents.
agents = destination / 'agents'
if agents.exists():
    shutil.rmtree(agents)
agents.mkdir()
shutil.copy2(root / 'agents/models.json', agents / 'models.json')
for name in ('AGENTS.md', 'README.md', 'LICENSE'):
    shutil.copy2(root / name, destination / name)
manifest = json.loads((root / '.codex-plugin/plugin.json').read_text())
(destination / 'plugin.json').write_text(json.dumps({key: manifest[key] for key in ('name', 'version', 'description')}, indent=2) + '\n')
(destination / 'rules').mkdir(exist_ok=True)
(destination / 'rules/atlas-core.md').write_text((root / 'core/ATLAS.md').read_text())
print(f'Antigravity: installed Atlas {manifest["version"]} at {destination}')
print('Skills and canonical doctrine installed; native hooks and custom-agent registration are not provided by this adapter.')
PY
