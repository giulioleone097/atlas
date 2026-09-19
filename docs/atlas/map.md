stamp: e6f1fc1 none 2026-09-08
# atlas - map

## Cosa fa, in una frase
Un plugin per Claude Code, Codex, Devin e Cursor, con adapter nativo di skill e regole per Antigravity che porta un lavoro dall'arrivo (issue, PR, idea) alla consegna (commit, PR, dossier) attraverso cinque fasi che si chiamano da sole (setup, scope, build, review, ship) più nove ingressi digitati per nome (atlasme, simplify, handoff, optimize, intel, question, howto, prototype, improve), quattro agenti, sette rilevatori e un banco di prova agentico, con una dottrina anti-slop attiva a ogni sessione. Per i cambi piccoli e compresi il percorso è implementazione, review, fix e prova; il ciclo completo resta per lavori ampi o incerti.

## Domini
- Dottrina: `core/ATLAS.md`, iniettata da `scripts/core-context.sh` via `hooks/claude-codex.json` (SessionStart, SubagentStart) su Claude Code e Codex; su Devin arriva via `AGENTS.md` del plugin (regola sempre attiva), su Cursor via `rules/atlas-core.mdc` (alwaysApply); su Antigravity come `rules/atlas-core.md` nel plugin globale. I blocchi in `AGENTS.md` e nel `.mdc` devono restare identici al core, `scripts/check.sh` lo verifica.
- Fasi: `skills/<stage>/SKILL.md` (<= 120 righe, router; descrizione che apre con "Use when", <= 70 parole) con `agents/openai.yaml` per Codex e `references/` (<= 80 righe) per ogni ramo: intake, atlasme, asking e `glossary.md` in scope; plan, debug, prove, e2e e i modi in build; shrink, slop, security, platform-native, audit e pr in review; dossier, shapes, evidence, posting, learn, environment in ship; map in setup; deepen in improve; metrics e worktrees in optimize; handoff, intel, question, howto e prototype senza rami, il corpo è la procedura. Raggiunte dagli host per nome e l'una dall'altra; Codex accorcia la descrizione a ~45 caratteri.
- Innesto del glossario: `atlasme` risolve un termine e lo innesta inline nel `CONTEXT.md` del repository bersaglio via `skills/scope/references/glossary.md`; `scope`, `build` e `setup` leggono `CONTEXT.md` come vocabolario già stabilito.
- Agenti: `agents/atlas-{scout,worker,reviewer,integrator}.md` dichiarano un tier (`sonnet`/`opus`); il modello per host sta in `agents/models.json`, letto dagli installer. Frontmatter unione (`tools:` Claude, `allowed-tools:` Devin, `readonly:` Cursor); su Codex generati in `~/.codex/agents/*.toml` da `scripts/install-codex-agents.sh`, su Devin caricati come subagent del plugin (`atlas:<name>`), su Cursor con `model:` riscritto a `inherit` dall'installer. Nel solo modo simulazione, l'attore vede esclusivamente il materiale fornito e non usa strumenti.
- Guardie: `scripts/guard.sh` (nega `--no-verify`, force push, `reset --hard`, scarti dell'intero albero, `rm -rf` della radice; legge `tool_input.command`, `text_input`/`bytes_input` o `command` e risponde con l'unione delle forme deny dei quattro host); fixture in `scripts/test-guard.sh`. File hook per famiglia: `hooks/claude-codex.json` (Claude+Codex), `hooks.json` alla radice (Devin), `hooks/cursor-hooks.json` (Cursor, dichiarato nel manifest).
- Rilevatori: `scripts/checks.sh` (comandi di verifica del progetto), `tracker.sh` (forge e CLI, con gh e glab sondati per un host enterprise o self-hosted), `consumers.sh` (repository dipendenti), `tokens.sh` (token di design), `repo-facts.sh` (fatti per la mappa), `debt.sh` (registro dei `ceiling:`), `pr-partition.py` (partizione del diff); `skills/ship/scripts/` tiene `pr-contracts.py`, `pr-walkthrough.py`, `test-summary.py`.
- Installer user-level: `scripts/install-devin.sh` e `scripts/install-cursor.sh` (skill come `atlas-<stage>` con riferimenti riscritti, agenti, dottrina/hook, idempotenti e reversibili con `--remove`) per dove il plugin manager non arriva. `scripts/install-antigravity.sh` installa skill/riferimenti/helper e dottrina in `~/.gemini/config/plugins/atlas`, senza registrazione di hook o agenti nativi.
- Evals: `evals/run.py` e `evals/tasks.py`, sei sonde in sessioni headless `--bare` con baseline, plugin corrente e plugin precedente opzionale, con riferimenti buono/cattivo; il selftest gira in `check.sh`, la corsa live richiede `ANTHROPIC_API_KEY` e le metriche mancanti restano non disponibili.
- Manifesti: `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `.devin-plugin/plugin.json`, `.cursor-plugin/plugin.json` (versioni pari), il manifest Antigravity `plugin.json` è derivato dal manifest Codex durante l’installazione; marketplace in `.claude-plugin/marketplace.json` e `.agents/plugins/marketplace.json`.

## Flusso principale
```
setup? -> scope (intake | atlasme | card) -> build (plan? | debug? | modo | prove) -> review (shrink, review locale o subagent utili, integrazione se serve) -> ship (commit, dossier, lesson)
```
Ingressi selezionabili anche automaticamente: `handoff` scrive dove sta il lavoro in `docs/handoff-*.md`, `scope <file>` lo riprende e `ship` lo cancella a lavoro committato; `optimize` propone KPI pertinenti e chiarisce priorità aperte con il tool nativo; sceglie comandi e opzioni dal contratto concordato, salvo override. Misura alternative in worktree isolati e combinazioni sul champion corrente entro un budget unico; snapshot privati preservano input non committati e indice. Integra il diff verificato e conserva il recupero fino alla prova finale e review.
Il ciclo sceglie il percorso: i cambi piccoli e compresi usano implementazione, review, fix e prova; i lavori ampi o incerti passano da `scope`, `build` e `review`. La review usa subagent economici solo quando aggiungono valore, senza un team minimo, e attribuisce le regressioni alla baseline dopo aver verificato i report.

Per ogni scelta materiale `scenarios.md` valuta il gate di interazione: scatta automaticamente solo se attori o sottosistemi distinti già forniti possono, con reazioni plausibili e fondate, cambiare fattibilità, scelta, priorità o esito; `--simulate` lo richiede esplicitamente senza inventare attori o fatti. Il chiamante mantiene l'unica simulazione interna: budget radice condiviso di tre onde di dispatch, profondità massima due, barriere per nodo/ramo/round/revisione, figli minimi per `INTERACTION` irrisolte e una sola review finale non partecipante. Stato, lineage, memoria e proposte restano nella mappa esistente.

## Confini
- I file hook non si condividono tra famiglie: `hooks/claude-codex.json` (Claude+Codex: SessionStart, SubagentStart con additionalContext, PreToolUse con permissionDecision), `hooks.json` radice (Devin: PreToolUse), `hooks/cursor-hooks.json` (Cursor: beforeShellExecution). Gli script rispondono a tutti con un unico payload multi-forma.
- Nessuna variabile di host dentro una skill o un agente: i percorsi sono relativi al file che li nomina (`<this skill>`, `<plugin root>`).
- Le skill sono host-neutrali; Codex non ha agenti nel plugin, quindi li riceve come agenti custom generati.

## Repository collegati
Nessuno: `scripts/consumers.sh` non trova manifesti che nominino questo repository.

## Controlli
- `sh scripts/check.sh`: quattro `claude plugin validate --strict`, 75 fixture del guard su tutte e quattro le forme di payload, 25 fixture di `core-context.sh`, la conformance degli installer eseguiti in una HOME usa-e-getta, JSON dei manifesti, sincronia della dottrina su AGENTS.md e rules/atlas-core.mdc, parità di versione sui quattro manifesti, eventi hook ammessi per host, regole del repository (limiti di righe, nessuna variabile di host, script che parsano, rilevatori che rispondono, descrizioni con il trigger in testa).
- `scripts/checks.sh` non trova un manifesto di progetto: il controllo canonico è `check.sh`.

## Stato della mappa
Refresh mirato del 2026-09-13 sul workflow e sugli adapter in preparazione della versione 2.0.5 (base c7ab1c6). Lo stamp iniziale resta la fonte delle osservazioni storiche non ricampionate; non indica la versione installata.

## Scorciatoie dichiarate
`sh scripts/debt.sh .`: quattro `ceiling:` nei rilevatori (tokens.sh 400 fogli di stile, consumers.sh profondità 4, repo-facts.sh tre chiamate gh per PR, tracker.sh host non loggato letto come forge=none), tutti con trigger di upgrade.

## Punti caldi
I quattro manifesti `.*-plugin/plugin.json` (ogni rilascio bumpa tutti e quattro), `README.md` e `docs/DESIGN.md` (ogni rilascio li aggiorna), `skills/ship/references/dossier.md` (il documento più riscritto: dossier v1 -> v6).

## Persone
Un solo autore nella finestra: Giulio Leone. Nessuna PR merged: il lavoro arriva su `main` per push diretto.

## Fonti
`scripts/repo-facts.sh . 12 0`, `scripts/consumers.sh .`, `scripts/checks.sh .`, lettura diretta dei file; nessun server di grafo o simboli usato per questa mappa.
