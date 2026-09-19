#!/bin/sh
# atlas test-guard: fixture suite for scripts/guard.sh. Feeds each command as
# PreToolUse(Bash) hook JSON on stdin; DENY commands must get a deny decision,
# ALLOW commands must produce no output. Prints one line per mismatch, then
# "guard: N/N ok"; exits 1 on any mismatch.

cd "$(dirname "$0")/.." || exit 1
pass=0
total=0

run() {
  total=$((total + 1))
  out=$(python3 -c 'import sys,json;sys.stdout.write(json.dumps({"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":sys.argv[1]}}))' "$1" | sh scripts/guard.sh)
  case "$out" in
    *'"permissionDecision": "deny"'*) got=deny ;;
    *) got=allow ;;
  esac
  if [ "$got" = "$2" ]; then pass=$((pass + 1)); else echo "FAIL (want $2, got $got): $1"; fi
}

NL='
'
DENY="git commit --no-verify -m x${NL}git -C /tmp/r commit --no-verify -m x${NL}/usr/bin/git reset --hard HEAD~1${NL}command /usr/bin/git reset --hard HEAD~1${NL}command -p /usr/bin/git reset --hard HEAD~1${NL}command -- /usr/bin/git reset --hard HEAD~1${NL}sh -c 'git reset --hard HEAD~1'${NL}bash -lc 'git reset --hard HEAD~1'${NL}eval 'git reset --hard HEAD~1'${NL}sh -c 'rm -rf \$HOME'${NL}echo ok && git push --no-verify${NL}git push --force origin main${NL}git push -f${NL}git push -uf origin main${NL}git push origin +main${NL}git reset --hard HEAD~1${NL}git clean -fdx${NL}git checkout .${NL}git checkout -- .${NL}git checkout HEAD -- .${NL}git checkout -f .${NL}git restore .${NL}git restore -- .${NL}git restore --staged --worktree .${NL}rm -rf /${NL}/bin/rm -rf /${NL}sh -c 'rm -rf /'${NL}rm -rf ~${NL}rm -rf ~/${NL}rm -rf \$HOME${NL}rm -rf \${HOME}${NL}rm -rf .${NL}rm -rf ..${NL}rm -rf *${NL}rm -rf /*${NL}rm -fr ./${NL}rm -r -f .${NL}echo x; rm -rf /"
ALLOW="command -v git${NL}command -V git${NL}echo 'git reset --hard HEAD~1'${NL}git commit -m \"document the --no-verify flag\"${NL}git commit -m \"cleanup | rm -rf . now\"${NL}npm test -- --no-verify-ssl${NL}git push --force-with-lease${NL}git push -u origin main${NL}git checkout main${NL}git checkout -b feature${NL}git restore --staged .${NL}git clean -n${NL}rm -rf node_modules${NL}rm -rf dist/${NL}rm -rf ./build${NL}rm -f file.txt${NL}ls -la${NL}git diff HEAD"

OLDIFS=$IFS
IFS=$NL
set -f
for line in $DENY; do run "$line" deny; done
for line in $ALLOW; do run "$line" allow; done
set +f
IFS=$OLDIFS

total=$((total + 1))
[ -z "$(printf '{not json' | sh scripts/guard.sh)" ] && pass=$((pass + 1)) || echo "FAIL: malformed JSON produced output"
total=$((total + 1))
[ -z "$(printf '' | sh scripts/guard.sh)" ] && pass=$((pass + 1)) || echo "FAIL: empty stdin produced output"

# The cases above all arrive as tool_input.command, the Claude/Codex shape. guard.sh also
# reads Devin write_to_process (text_input, bytes_input) and Cursor beforeShellExecution
# (command at top level); a regression in those branches would ship silently otherwise.
# shape <label> <python expression building the payload from argv[1]> <want deny|allow>
shape() {
  total=$((total + 1))
  out=$(python3 -c "import sys,json;sys.stdout.write(json.dumps($2))" "$3" | sh scripts/guard.sh)
  case "$out" in
    *'"permissionDecision": "deny"'*) got=deny ;;
    *) got=allow ;;
  esac
  if [ "$got" = "$4" ]; then pass=$((pass + 1)); else echo "FAIL (want $4, got $got): $1"; fi
}

CLAUDE_SHAPE='{"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":sys.argv[1]}}'
TEXT_SHAPE='{"hook_event_name":"PreToolUse","tool_name":"write_to_process","tool_input":{"text_input":sys.argv[1]}}'
BYTES_SHAPE='{"hook_event_name":"PreToolUse","tool_name":"write_to_process","tool_input":{"bytes_input":sys.argv[1]}}'
CURSOR_SHAPE='{"command":sys.argv[1],"cwd":"/tmp"}'

for s in "$CLAUDE_SHAPE" "$TEXT_SHAPE" "$BYTES_SHAPE" "$CURSOR_SHAPE"; do
  shape "deny via $s" "$s" 'git push --force origin main' deny
  shape "deny via $s" "$s" 'rm -rf /' deny
  shape "allow via $s" "$s" 'git push -u origin main' allow
  shape "allow via $s" "$s" 'ls -la' allow
done

# One payload has to answer every host: each reads the field it knows, and a host whose
# field is missing sees no denial at all.
total=$((total + 1))
missing=$(printf '{"tool_input":{"command":"rm -rf /"}}' | sh scripts/guard.sh | python3 -c "
import sys, json
d = json.load(sys.stdin)
want = {
    'claude/codex': d.get('hookSpecificOutput', {}).get('permissionDecision') == 'deny',
    'devin': d.get('decision') == 'block' and bool(d.get('reason')),
    'cursor': d.get('permission') == 'deny' and bool(d.get('user_message')),
}
print(','.join(k for k, ok in want.items() if not ok))")
if [ -z "$missing" ]; then pass=$((pass + 1)); else echo "FAIL: deny payload missing host fields: $missing"; fi

if [ "$pass" -eq "$total" ]; then
  echo "guard: $pass/$total ok"
else
  echo "guard: $pass/$total"
  exit 1
fi
