#!/bin/sh
# atlas: detect the work tracker this repository actually has, with no plugin,
# no MCP server and no configuration. Prints one key=value per line:
#   declared <name> | none                      (a line `atlas: tracker=<name> [project=<x>]` in the nearest
#                                                AGENTS.md or CLAUDE.md, this directory upward to /)
#   project  <value> | -                        (the container named on that same line)
#   forge    github | gitlab | azure | none     (from the origin remote; another host is probed through gh, then glab)
#   cli      gh | glab | az | none              (the binary that is installed)
#   auth     ok | missing | unknown             (whether that binary is logged in)
#   repo     owner/name | project path | -      (what the cli needs to address it)
#   local    <dir>                              (fallback: tickets as files)
# The declaration selects the store; detection only offers a candidate, and neither is
# write authority. Only the first token after tracker= is read; an empty value reads `declared=none`.
# The walk stops below the home directory: a declaration is per repository or project folder, never machine-wide.
# `cli=none` or `auth=missing` is not an error: the caller falls back to `local`.
# Any read here is read-only; nothing is created.

cd -P "${1:-.}" 2>/dev/null || { echo "declared=none"; echo "project=-"; echo "forge=none"; echo "cli=none"; echo "auth=unknown"; echo "repo=-"; echo "local=docs/tickets"; exit 0; }

declared=none; project=-
dir=$(pwd -P); line=""; home=$(cd -P "${HOME:-/}" 2>/dev/null && pwd -P)
while [ -z "$line" ]; do
  for f in "$dir/AGENTS.md" "$dir/CLAUDE.md"; do
    [ -f "$f" ] || continue
    line=$(sed -n '/^atlas: tracker=/{p;q;}' "$f" 2>/dev/null | tr -d '\r')
    [ -n "$line" ] && break
  done
  [ -n "$line" ] && break
  [ "$dir" = "/" ] && break
  dir=$(dirname "$dir")
  [ "$dir" = "${home:-/}" ] && break
done
set -f  # $line is split on purpose; no token of it is a glob
for tok in $line; do
  case "$tok" in
    tracker=?*) declared=${tok#tracker=} ;;
    project=?*) project=${tok#project=} ;;
  esac
done
set +f
case "$declared" in *[!A-Za-z0-9._-]*) declared=none ;; esac
case "$project" in *[!A-Za-z0-9._/-]*) project=- ;; esac
[ "$declared" = none ] && project=-

url=$(git remote get-url origin 2>/dev/null || echo "")
forge=none; cli=none; auth=unknown; repo=-

case "$url" in
  *github.com[:/]*)
    forge=github
    repo=$(printf '%s' "$url" | sed -e 's#.*github\.com[:/]##' -e 's#\.git$##')
    if command -v gh >/dev/null 2>&1; then
      cli=gh
      if gh auth status >/dev/null 2>&1; then auth=ok; else auth=missing; fi
    fi
    ;;
  *gitlab*)
    forge=gitlab
    repo=$(printf '%s' "$url" | sed -e 's#.*gitlab[^:/]*[:/]##' -e 's#\.git$##')
    if command -v glab >/dev/null 2>&1; then
      cli=glab
      if glab auth status >/dev/null 2>&1; then auth=ok; else auth=missing; fi
    fi
    ;;
  *dev.azure.com*|*visualstudio.com*)
    forge=azure
    repo=$(printf '%s' "$url" | sed -e 's#^.*[:/]v3/##' -e 's#.*dev\.azure\.com/##' -e 's#.*@##' -e 's#/_git/#/#' -e 's#\.git$##')
    if command -v az >/dev/null 2>&1; then
      cli=az
      if az account show >/dev/null 2>&1; then auth=ok; else auth=missing; fi
    fi
    ;;
  ?*)
    # an enterprise GitHub or a self-hosted GitLab under another name: gh and glab resolve the host
    # from the remote themselves, and a host they do not know fails fast with no network call.
    # ceiling: a host gh or glab is installed for but not logged into reads forge=none, not auth=missing, upgrade when a user reports one
    repo=$(printf '%s' "$url" | sed -e 's#^[a-z+]*://[^/]*/##' -e 's#^[^/]*:##' -e 's#\.git$##')
    if command -v gh >/dev/null 2>&1 && gh repo view --json nameWithOwner >/dev/null 2>&1; then
      forge=github; cli=gh; auth=ok
    elif command -v glab >/dev/null 2>&1 && glab repo view >/dev/null 2>&1; then
      forge=gitlab; cli=glab; auth=ok
    else
      repo=-
    fi
    ;;
esac

echo "declared=$declared"
echo "project=$project"
echo "forge=$forge"
echo "cli=$cli"
echo "auth=$auth"
echo "repo=$repo"
echo "local=docs/tickets"
