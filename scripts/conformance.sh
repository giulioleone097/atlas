#!/bin/sh
# atlas conformance: execute every user-level installer into a throwaway HOME and assert
# the tree it actually produces. check.sh proves the sources parse and exist; this proves
# the delivery works. Every user-facing failure this repo has shipped came from here.
# Prints one line per mismatch, then "conformance: N/N ok"; exits 1 on any mismatch.
# No network, no API key: each installer only copies and rewrites local files.

cd "$(dirname "$0")/.." || exit 1
ROOT=$(pwd)
pass=0
total=0

TMP=$(mktemp -d) || exit 1
trap 'rm -rf "$TMP"' EXIT
HOME="$TMP/home"; export HOME
CODEX_HOME="$HOME/.codex"; export CODEX_HOME
unset XDG_CONFIG_HOME
mkdir -p "$HOME"

STAGES=$(ls -1 "$ROOT/skills")
NSTAGES=$(printf '%s\n' "$STAGES" | wc -l | tr -d ' ')
NAGENTS=$(ls -1 "$ROOT"/agents/atlas-*.md | wc -l | tr -d ' ')

ok() { total=$((total + 1)); pass=$((pass + 1)); }
no() { total=$((total + 1)); echo "FAIL: $1"; }
# check <description> <test-expression...>
check() { d=$1; shift; if "$@"; then ok; else no "$d"; fi; }

# doctrine_current <file> — the installed copy must be the doctrine we ship, not a frozen one
doctrine_current() {
  python3 - "$1" "$ROOT/core/ATLAS.md" <<'PY'
import sys
inst, core = (open(p).read() for p in sys.argv[1:3])
raise SystemExit(0 if core.strip() in inst else 1)
PY
}

# ---------------------------------------------------------------- Devin
sh "$ROOT/scripts/install-devin.sh" >"$TMP/devin.log" 2>&1 || no "install-devin.sh exited non-zero"
D="$HOME/.config/devin"
n=$(ls -1d "$D"/skills/atlas-*/ 2>/dev/null | wc -l | tr -d ' ')
check "devin installed $n skills, repo has $NSTAGES" [ "$n" = "$NSTAGES" ]
for s in $STAGES; do
  [ -f "$D/skills/atlas-$s/SKILL.md" ] || { no "devin missing skill atlas-$s"; continue; }
  ok
done
n=$(ls -1 "$D"/agents/atlas-*.md 2>/dev/null | wc -l | tr -d ' ')
check "devin installed $n agents, repo has $NAGENTS" [ "$n" = "$NAGENTS" ]
check "devin AGENTS.md carries the doctrine" [ -f "$D/AGENTS.md" ]
[ -f "$D/AGENTS.md" ] && { doctrine_current "$D/AGENTS.md" && ok || no "devin doctrine copy is not core/ATLAS.md"; }
check "devin config.json written" [ -f "$D/config.json" ]
[ -f "$D/config.json" ] && { grep -q 'guard.sh' "$D/config.json" && ok || no "devin config.json does not wire guard.sh"; }
# The installer rewrites cross-skill references from atlas:<stage> to atlas-<stage>; a
# missed one is a dead handoff on that host. Marker comments (atlas:core, atlas:narrate,
# atlas:fill) are not skill references and must survive untouched.
left=$(for s in $STAGES; do grep -rlsF "atlas:$s" "$D/skills"; done | sort -u)
if [ -n "$left" ]; then no "devin skills still name atlas:<stage>: $(echo "$left" | tr '\n' ' ')"; else ok; fi
# Its own summary line must not go stale against the tree it just wrote.
if grep -qs "$NAGENTS agents" "$TMP/devin.log"; then ok; else no "devin installer reports the wrong agent count: $(tail -1 "$TMP/devin.log")"; fi

sh "$ROOT/scripts/install-devin.sh" --remove >/dev/null 2>&1 || no "install-devin.sh --remove exited non-zero"
n=$(ls -1d "$D"/skills/atlas-*/ 2>/dev/null | wc -l | tr -d ' ')
check "devin --remove left $n skills behind" [ "$n" = "0" ]
if [ -f "$D/config.json" ] && grep -q 'guard.sh' "$D/config.json"; then no "devin --remove left the hook wired"; else ok; fi

# ---------------------------------------------------------------- Cursor
sh "$ROOT/scripts/install-cursor.sh" >"$TMP/cursor.log" 2>&1 || no "install-cursor.sh exited non-zero"
C="$HOME/.cursor"
n=$(ls -1d "$C"/skills/atlas-*/ 2>/dev/null | wc -l | tr -d ' ')
check "cursor installed $n skills, repo has $NSTAGES" [ "$n" = "$NSTAGES" ]
n=$(ls -1 "$C"/agents/atlas-*.md 2>/dev/null | wc -l | tr -d ' ')
check "cursor installed $n agents, repo has $NAGENTS" [ "$n" = "$NAGENTS" ]
# Cursor cannot resolve Claude/Devin model names; the installer must rewrite every one.
if grep -rhs '^model:' "$C"/agents/atlas-*.md | grep -qv '^model: inherit$'; then
  no "cursor agents keep a model: the host cannot resolve"
else ok; fi
check "cursor hooks.json written" [ -f "$C/hooks.json" ]
[ -f "$C/hooks.json" ] && { grep -q 'beforeShellExecution' "$C/hooks.json" && ok || no "cursor hooks.json has no beforeShellExecution"; }
left=$(for s in $STAGES; do grep -rlsF "atlas:$s" "$C/skills"; done | sort -u)
if [ -n "$left" ]; then no "cursor skills still name atlas:<stage>: $(echo "$left" | tr '\n' ' ')"; else ok; fi

sh "$ROOT/scripts/install-cursor.sh" --remove >/dev/null 2>&1 || no "install-cursor.sh --remove exited non-zero"
n=$(ls -1d "$C"/skills/atlas-*/ 2>/dev/null | wc -l | tr -d ' ')
check "cursor --remove left $n skills behind" [ "$n" = "0" ]

# ---------------------------------------------------------------- Codex agents
sh "$ROOT/scripts/install-codex-agents.sh" >/dev/null 2>&1 || no "install-codex-agents.sh exited non-zero"
n=$(ls -1 "$CODEX_HOME"/agents/*.toml 2>/dev/null | wc -l | tr -d ' ')
check "codex generated $n agent TOMLs, repo has $NAGENTS" [ "$n" = "$NAGENTS" ]
# A generated file the host cannot parse is a silently missing agent.
python3 - "$CODEX_HOME/agents" "$ROOT/agents" <<'PY' && ok || no "generated Codex agents are not valid or lose a field"
import glob, os, re, sys, tomllib
dest, src = sys.argv[1], sys.argv[2]
bad = []
for path in sorted(glob.glob(os.path.join(dest, "*.toml"))):
    try:
        d = tomllib.load(open(path, "rb"))
    except Exception as e:
        bad.append(f"{os.path.basename(path)}: unparseable ({e})"); continue
    for key in ("name", "description", "developer_instructions"):
        if not d.get(key):
            bad.append(f"{os.path.basename(path)}: missing {key}")
    if not d.get("developer_instructions", "").strip():
        bad.append(f"{os.path.basename(path)}: empty body")
# every read-only agent must land sandboxed, or it can write on Codex
for path in sorted(glob.glob(os.path.join(src, "*.md"))):
    text = open(path).read()
    m = re.search(r"^tools:\s*(.*)$", text, re.M)
    if m and not re.search(r"\b(Edit|Write)\b", m.group(1)):
        name = os.path.basename(path)[:-3].replace("-", "_")
        gen = os.path.join(dest, name + ".toml")
        if not os.path.exists(gen):
            bad.append(f"{name}: not generated"); continue
        if tomllib.load(open(gen, "rb")).get("sandbox_mode") != "read-only":
            bad.append(f"{name}: read-only agent generated without sandbox_mode")
if bad:
    print("  " + "\n  ".join(bad), file=sys.stderr)
raise SystemExit(1 if bad else 0)
PY

# ---------------------------------------------------------------- Antigravity
sh "$ROOT/scripts/install-antigravity.sh" >/dev/null 2>&1 || no "install-antigravity.sh exited non-zero"
A="$HOME/.gemini/config/plugins/atlas"
n=$(ls -1d "$A"/skills/*/ 2>/dev/null | wc -l | tr -d ' ')
check "antigravity installed $n skills, repo has $NSTAGES" [ "$n" = "$NSTAGES" ]
check "antigravity doctrine rule written" [ -f "$A/rules/atlas-core.md" ]
[ -f "$A/rules/atlas-core.md" ] && { doctrine_current "$A/rules/atlas-core.md" && ok || no "antigravity doctrine copy is not core/ATLAS.md"; }
check "antigravity manifest written" [ -f "$A/plugin.json" ]
[ -f "$A/plugin.json" ] && { python3 -c "
import json,sys
m=json.load(open(sys.argv[1])); r=json.load(open(sys.argv[2]))
raise SystemExit(0 if m.get('version')==r.get('version') and m.get('name')==r.get('name') else 1)
" "$A/plugin.json" "$ROOT/.codex-plugin/plugin.json" && ok || no "antigravity manifest drifted from the source manifest"; }
# The adapter deliberately ships no agents; it must also not ship a half-set.
n=$(ls -1 "$A"/agents/*.md 2>/dev/null | wc -l | tr -d ' ')
check "antigravity shipped $n agent files, expected 0" [ "$n" = "0" ]

if [ "$pass" -eq "$total" ]; then
  echo "conformance: $pass/$total ok"
else
  echo "conformance: $pass/$total"
  exit 1
fi
