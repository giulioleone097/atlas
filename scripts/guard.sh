#!/bin/sh
# atlas guard: pre-execution shell hook for Claude Code (PreToolUse Bash),
# Codex (same), Devin (PreToolUse exec/write_to_process) and Cursor
# (beforeShellExecution). Denies a fixed list of destructive git/rm commands
# anywhere in the command string, including after &&, ;, |.
# See docs/DESIGN.md "Hooks" for the rule table. Any parse or unexpected
# error: print nothing, exit 0 -- never trap the user.

exec python3 -c '
import sys, json, os, re, shlex

def allow():
    sys.exit(0)

def deny(reason):
    msg = "atlas guard: " + reason
    # one payload, every host reads the fields it knows:
    # Claude Code/Codex -> hookSpecificOutput.permissionDecision
    # Devin             -> decision + reason
    # Cursor            -> permission + user_message/agent_message
    payload = {
        "decision": "block",
        "reason": msg,
        "permission": "deny",
        "user_message": msg,
        "agent_message": msg,
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": msg,
        },
    }
    sys.stdout.write(json.dumps(payload))
    sys.exit(0)

try:
    raw = sys.stdin.read()
    data = json.loads(raw)
except Exception:
    allow()

# Claude/Devin send tool_input.command; Devin write_to_process sends
# text_input/bytes_input; Cursor beforeShellExecution sends command at top level.
ti = data.get("tool_input") if isinstance(data, dict) else None
if not isinstance(ti, dict):
    ti = {}
cmd = (
    ti.get("command")
    or ti.get("text_input")
    or ti.get("bytes_input")
    or (data.get("command") if isinstance(data, dict) else None)
    or ""
)

if not isinstance(cmd, str) or not cmd.strip():
    allow()

OPERATORS = set("&|;()")
FORBIDDEN_RM_TARGETS = {"/", "~", "$HOME", ".", "..", "*"}
ASSIGNMENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*=.*")
SHELLS = {"sh", "bash", "dash", "zsh", "ksh"}

def parse(command):
    lexer = shlex.shlex(command, posix=True, punctuation_chars=True)
    lexer.wordchars += "${}"
    tokens = list(lexer)
    segments = [[]]
    for token in tokens:
        if token and set(token) <= OPERATORS:
            segments.append([])
        else:
            segments[-1].append(token)
    return segments

def executable(segment):
    index = 0
    while index < len(segment) and ASSIGNMENT.fullmatch(segment[index]):
        index += 1
    while index < len(segment):
        wrapper = os.path.basename(segment[index])
        if wrapper == "command":
            index += 1
            if index < len(segment) and segment[index] in {"-v", "-V"}:
                return "", []
            if index < len(segment) and segment[index] == "-p":
                index += 1
            if index < len(segment) and segment[index] == "--":
                index += 1
            continue
        if wrapper == "exec":
            index += 1
            continue
        break
    if index >= len(segment):
        return "", []
    return os.path.basename(segment[index]), segment[index + 1:]

def inspect(command):
    try:
        segments = parse(command)
    except ValueError:
        return

    for segment in segments:
        if not segment:
            continue
        name, rest = executable(segment)

        if name in SHELLS:
            for index, flag in enumerate(rest):
                if flag == "-c" or (flag.startswith("-") and not flag.startswith("--") and "c" in flag[1:]):
                    if index + 1 < len(rest) and len(rest[index + 1]) < len(command):
                        inspect(rest[index + 1])
                    break
            continue
        if name == "eval":
            payload = " ".join(rest)
            if payload and len(payload) < len(command):
                inspect(payload)
            continue

        if name == "git":
            if "--no-verify" in rest:
                deny("--no-verify bypasses git hooks")

            if "push" in rest:
                pi = rest.index("push")
                after = rest[pi + 1:]
                for token in after:
                    if token == "--force":
                        deny("git push --force can overwrite remote history; use --force-with-lease")
                    if token.startswith("-") and not token.startswith("--") and "f" in token:
                        deny("git push -f can overwrite remote history; use --force-with-lease")
                    if token.startswith("+"):
                        deny("git push +refspec forces the update; use --force-with-lease")

            if "reset" in rest and "--hard" in rest:
                deny("git reset --hard discards uncommitted work")

            if "clean" in rest:
                has_force = "--force" in rest or any(
                    token.startswith("-") and not token.startswith("--") and "f" in token
                    for token in rest
                )
                if has_force:
                    deny("git clean -f deletes untracked files with no undo")

            if "checkout" in rest:
                ci = rest.index("checkout")
                tail = rest[ci + 1:]
                if "." in tail:
                    deny("git checkout . discards working-tree changes")

            if "restore" in rest:
                ri = rest.index("restore")
                tail = rest[ri + 1:]
                if "." in tail:
                    staged_only = ("--staged" in tail or "-S" in tail) and not (
                        "--worktree" in tail or "-W" in tail
                    )
                    if not staged_only:
                        deny("git restore . discards working-tree changes")

        if name == "rm":
            flags = [token for token in rest if token.startswith("-")]
            args = [token for token in rest if not token.startswith("-")]
            short_letters = "".join(flag.lstrip("-") for flag in flags if not flag.startswith("--"))
            long_flags = set(token for token in flags if token.startswith("--"))
            recursive = "r" in short_letters or "R" in short_letters or "--recursive" in long_flags
            force = "f" in short_letters or "--force" in long_flags
            if recursive and force:
                for arg in args:
                    norm = arg.replace("${HOME}", "$HOME")
                    if norm.endswith("/*"):
                        norm = norm[:-2]
                    norm = norm.rstrip("/") or "/"
                    if norm in FORBIDDEN_RM_TARGETS:
                        deny("rm -rf " + arg + " is a catastrophic delete target")

inspect(cmd)

allow()
'
