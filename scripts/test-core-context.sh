#!/bin/sh
# atlas test-core-context: fixture suite for scripts/core-context.sh, the hook that
# delivers the doctrine. Each case feeds one payload on stdin in a scratch tree and
# asserts inject or suppress. Prints one line per mismatch, then "core-context: N/N ok";
# exits 1 on any mismatch. The guard has had fixtures since it shipped; this is the
# same shape for the other half of the delivery path.

cd "$(dirname "$0")/.." || exit 1
ROOT=$(pwd)
CORE="$ROOT/core/ATLAS.md"
pass=0
total=0

TMP=$(mktemp -d) || exit 1
trap 'rm -rf "$TMP"' EXIT
# A HOME with no global rules file, so home-global suppression never fires by accident.
HOME="$TMP/home"; export HOME
mkdir -p "$HOME"

# run <name> <cwd> <payload> <want: inject|suppress>
run() {
  total=$((total + 1))
  out=$(cd "$2" && printf '%s' "$3" | sh "$ROOT/scripts/core-context.sh" 2>/dev/null)
  if [ -n "$out" ]; then got=inject; else got=suppress; fi
  if [ "$got" = "$4" ]; then
    pass=$((pass + 1))
  else
    echo "FAIL (want $4, got $got): $1"
  fi
}

# field <payload> <python expression over the parsed object>
field() {
  total=$((total + 1))
  out=$(printf '%s' "$2" | sh "$ROOT/scripts/core-context.sh" 2>/dev/null)
  got=$(printf '%s' "$out" | python3 -c "import sys,json
try:
    d = json.load(sys.stdin)
except Exception:
    print('<no json>'); raise SystemExit
print($3)" 2>/dev/null)
  if [ "$got" = "$4" ]; then
    pass=$((pass + 1))
  else
    echo "FAIL (want $4, got $got): $1"
  fi
}

SS='{"hook_event_name":"SessionStart"}'
START='<!-- atlas:core:start -->'
END='<!-- atlas:core:end -->'
LEGACY_START='<!-- sniper:core:start -->'
LEGACY_END='<!-- sniper:core:end -->'

# A bare tree with no project instructions gets the doctrine.
mkdir -p "$TMP/bare"
run "bare tree" "$TMP/bare" "$SS" inject

# A project carrying the CURRENT doctrine already loads it; injecting would cost it twice.
mkdir -p "$TMP/current"
{ printf '# p\n\n%s\n' "$START"; cat "$CORE"; printf '%s\n' "$END"; } > "$TMP/current/AGENTS.md"
run "AGENTS.md carries current doctrine" "$TMP/current" "$SS" suppress

# CLAUDE.md is read the same way.
mkdir -p "$TMP/current-claude"
{ printf '# p\n\n%s\n' "$START"; cat "$CORE"; printf '%s\n' "$END"; } > "$TMP/current-claude/CLAUDE.md"
run "CLAUDE.md carries current doctrine" "$TMP/current-claude" "$SS" suppress

# The regression this suite exists for: a frozen block from an older install must NOT
# suppress the doctrine it is out of date with, or the update never reaches the user.
mkdir -p "$TMP/stale"
printf '# p\n\n%s\nOLD DOCTRINE, frozen at install time.\n%s\n' "$START" "$END" > "$TMP/stale/AGENTS.md"
run "stale block does not suppress the update" "$TMP/stale" "$SS" inject

# Same rule for the pre-rename marker pair.
mkdir -p "$TMP/legacy-stale"
printf '# p\n\n%s\nOLD DOCTRINE.\n%s\n' "$LEGACY_START" "$LEGACY_END" > "$TMP/legacy-stale/AGENTS.md"
run "stale sniper block does not suppress" "$TMP/legacy-stale" "$SS" inject

# A pre-rename block whose text is current is still current.
mkdir -p "$TMP/legacy-current"
{ printf '# p\n\n%s\n' "$LEGACY_START"; cat "$CORE"; printf '%s\n' "$LEGACY_END"; } > "$TMP/legacy-current/AGENTS.md"
run "current sniper block suppresses" "$TMP/legacy-current" "$SS" suppress

# An opening marker with no closing marker cannot be verified, so it is not trusted.
mkdir -p "$TMP/unterminated"
printf '# p\n\n%s\n' "$START" > "$TMP/unterminated/AGENTS.md"
run "unterminated block is not trusted" "$TMP/unterminated" "$SS" inject

# The hook runs in the session cwd, which may be a subdirectory of the project.
mkdir -p "$TMP/current/sub/deeper"
run "block found up the tree" "$TMP/current/sub/deeper" "$SS" suppress

# cwd from the payload wins over the process cwd.
run "payload cwd is used" "$TMP/bare" "{\"hook_event_name\":\"SessionStart\",\"cwd\":\"$TMP/current\"}" suppress

# A host-global rules file carrying the current doctrine suppresses too.
mkdir -p "$HOME/.claude"
{ printf '%s\n' "$START"; cat "$CORE"; printf '%s\n' "$END"; } > "$HOME/.claude/CLAUDE.md"
run "home-global current block suppresses" "$TMP/bare" "$SS" suppress
printf '%s\nOLD.\n%s\n' "$START" "$END" > "$HOME/.claude/CLAUDE.md"
run "home-global stale block does not" "$TMP/bare" "$SS" inject
rm -f "$HOME/.claude/CLAUDE.md"

# Cursor sends no hook_event_name and reads none of those files, so the home check is
# skipped there: a home-global block must not silence Cursor.
mkdir -p "$HOME/.claude"
{ printf '%s\n' "$START"; cat "$CORE"; printf '%s\n' "$END"; } > "$HOME/.claude/CLAUDE.md"
run "cursor ignores home-global block" "$TMP/bare" '{"composer_mode":"agent"}' inject
rm -f "$HOME/.claude/CLAUDE.md"

# Unreadable stdin still delivers the doctrine rather than silently dropping it.
run "malformed stdin still injects" "$TMP/bare" 'not json at all' inject
run "empty stdin still injects" "$TMP/bare" '' inject
# ...but it must still honour a project that already carries the doctrine.
run "malformed stdin honours current block" "$TMP/current" 'not json at all' suppress

# ATLAS_SUBAGENT_MATCHER narrows which subagents receive the doctrine. A var= prefix on a
# function call has unspecified persistence in POSIX sh, so each matcher is set and cleared
# explicitly rather than relying on the shell.
SUB='{"hook_event_name":"SubagentStart","agent_type":"atlas-scout"}'
# matcher <var> <value> <label> <want>
matcher() {
  export "$1=$2"
  run "$3" "$TMP/bare" "$SUB" "$4"
  unset "$1"
}
run "subagent without matcher" "$TMP/bare" "$SUB" inject
matcher ATLAS_SUBAGENT_MATCHER scout "subagent matching" inject
matcher ATLAS_SUBAGENT_MATCHER nomatch "subagent not matching" suppress
matcher ATLAS_SUBAGENT_MATCHER '[' "bad matcher regex is ignored" inject
matcher SNIPER_SUBAGENT_MATCHER nomatch "legacy matcher still honored" suppress

# Every host reads the field it knows, from one payload.
cd "$TMP/bare" || exit 1
field "claude/codex/devin field" "$SS" "d['hookSpecificOutput']['additionalContext'][:10]" "ATLAS CORE"
field "cursor field" "$SS" "d['additional_context'][:10]" "ATLAS CORE"
field "event echoed back" '{"hook_event_name":"SubagentStart"}' "d['hookSpecificOutput']['hookEventName']" "SubagentStart"
field "event defaults to SessionStart" '{}' "d['hookSpecificOutput']['hookEventName']" "SessionStart"
# The doctrine travels as additionalContext: Claude Code cuts it at 10,000 characters and
# Codex near 2,500 tokens. check.sh gates the file; this gates what is actually transmitted.
field "transmitted under 10,000 chars" "$SS" "len(d['hookSpecificOutput']['additionalContext']) < 10000" "True"
cd "$ROOT" || exit 1

if [ "$pass" -eq "$total" ]; then
  echo "core-context: $pass/$total ok"
else
  echo "core-context: $pass/$total"
  exit 1
fi
