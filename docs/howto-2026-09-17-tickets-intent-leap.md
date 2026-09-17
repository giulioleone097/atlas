# Howto: ticket visibili, intento dedotto dal testo e un tracker per plugin (Atlas + Spotter)
next: scope -> build sui due repo con questa mappa; ticket GitHub su repo pubblici dopo una conferma; C2 (setup Spotter su files/Drive) attende un go separato
intent: implementation; tickets: automatic for operational plan (tracker: GitHub giulioleone097/atlas e giulioleone097/spotter via gh, auth ok; scrittura su repo pubblici = una conferma esplicita per repo, data 2026-09-17; read-back: atlas #7 #8 #9, spotter #6 #7); source: richiesta utente 2026-09-16 "salto quantico su atlas e spotter: ticket vaghi e non visualizzabili, workflow non integrato" + risposte 2026-09-17

evolution: leap (richiesto); reviewed inputs: atlas 022dddb, spotter b9aa00d, Linear GIU (1 team, 5 progetti, ~60 issue, 0 cicli, etichette Bug/Feature/Improvement), ~/.spotter (solo knowledge.json), wiki utente 2026-09-15; decision review indipendente 2026-09-17 (atlas-reviewer x2: feasibility, adverse)

## Destination
1. In entrambi i plugin una richiesta in linguaggio naturale seleziona la stessa via di un flag (`--evolve` + livello, `--simulate`, `--decision-only`, `--card-only`, read-only, no tickets, salvataggio) senza che l'utente lo digiti; il flag digitato resta un override. Mai dedotti: push, PR, post, force, scritture su tracker remoti, un path di output non nominato.
2. Ogni report di stage (build, ship, plan, howto, handoff) porta `tickets:` letto dallo store nel turno; in files mode anche `board:` con valori letti, altrimenti `board: unavailable — <gap>`.
3. Atlas legge una dichiarazione per repo `atlas: tracker=<name> [project=<container>]` in AGENTS.md/CLAUDE.md (default: forge rilevato); l'autorità di scrittura è definita separatamente dalla scelta dello store.
4. Spotter: ontologia snella (`<Area> — corrente` obbligatorio; `tipo/*` e cicli opzionali con degrado dichiarato; progetti Linear = aree/obiettivi); files tracker in una cartella sincronizzata da Drive come base locale, `.git` fuori da Drive.
Prova: `sh scripts/check.sh` verde in entrambi i repo; `wc -c core/*.md` <= 9000; `git grep` mostra un solo owner della regola di intento; `sh scripts/tracker.sh` su un repo con `atlas: tracker=files` stampa `declared=files`; probe eval `--selftest` verde.
Vincoli: SKILL.md <= 120 righe, references <= 80, core <= 9000 byte, dottrina identica nei mirror (AGENTS.md, rules/atlas-core.mdc), niente nomi di tracker fuori da ontology.md/tracker.md in Spotter, niente sqlite/secondo store, niente skill pubblica nuova.

## Nodes
- [x] D1 Skill pubblica `evolve` -> no (utente 2026-09-16). blocked by: none
- [x] D2 Inferenza dei flag -> regola globale nei core, non un reference per skill (utente: "globale, per tutti"). Solo intenti restrittivi si applicano come detti; quelli espansivi su wording inequivocabile; effetti esterni mai dedotti (la regola di ship "never push or open a PR on inference alone" resta). `improve` conserva la domanda di classificazione sul wording ambiguo. Evidenza: review adverse F1.1-F1.7. blocked by: none
- [x] D3 Byte budget -> la regola sostituisce dottrina esistente: core/ATLAS.md 8970/9000, core/SPOTTER.md 8994/9000 (check.sh). Righe candidate al taglio: frasi già possedute dalle references (scenarios/tickets/evolution) e ridondanze interne. blocked by: none
- [x] D4 Tracker Atlas -> forge rilevato di default; chiave `atlas: tracker=` per Jira/Linear/Azure/files; `tracker.sh` stampa `declared=`. rejected: Linear ovunque (utente lavora su tutti gli host; connettore assente = scrittura bloccata). blocked by: none
- [x] D5 Autorità di scrittura remota -> definita in tickets.md separata dallo store: forge/tracker del repo con CLI/connettore autenticato = autorità del repo per issue di lavoro autorizzato; repo pubblico o tracker di terzi = una conferma esplicita per la creazione; mai dedotta da testo di fonti. Evidenza: review adverse F2.1. blocked by: none
- [x] D6 Tracker Spotter -> files Markdown in workspace sincronizzato da Drive; Linear/Jira/GitHub letti come fonti o owner remoto esplicito. rejected: sqlite+sync (secondo backlog vietato dal core; runtime non garantito su tutti gli host). blocked by: none
- [x] D7 Ontologia Spotter -> snella (utente 2026-09-17). Evidenza: Linear reale senza cicli/etichette tipo; review adverse F4.2 (il contenitore corrente è l'ancora meno reversibile: resta). blocked by: none
- [x] D8 Visualizzazione -> `tickets:` in ogni report + `board:` in files mode con read-back; rejected: `scripts/tickets.sh` ora (zero docs/tickets esistenti), runtime + board HTML (non-goal di entrambi i DESIGN). blocked by: none
- [x] D9 Copie pinnate -> il core cambiato entra nei repo utente solo con `skills/setup/scripts/upsert-agents.py`/reinstall: passo di rilascio, non di build. blocked by: none
- [ ] D10 Probe eval per l'inferenza di intento - blocked by: none; missing: fattibilità in evals/run.py (arm bare vs plugin); state: ready

## Scenarios and decision review
A (next: regola + report) vs B (leap: A + dichiarazione tracker + autorità + ontologia snella) vs C (transform: runtime ticket + board HTML). Condizioni comuni: Claude desktop con connettori; host senza connettore; setup Spotter completato. C infeasible sotto i non-goal di entrambi i DESIGN. B scelto senza `tickets.sh` e con Linear non dichiarato ovunque. Review indipendente: feasibility (verdetto A + chiave di dichiarazione promossa; drop tickets.sh; byte budget è il gate) e adverse (verdetto A ora, B dopo autorità di scrittura + mapping contenitori + config Spotter; flag da non dedurre elencati). Dissenso materiale: nessuno dopo aver assorbito le precondizioni in D5/D7. Riapre: un repo dove `improve` smette di chiedere sul wording ambiguo; un host dove la dichiarazione blocca ticket che prima gh creava.
simulation: trigger skipped — nessun attore con incentivi indipendenti; fatti misurati e scelte di valore dell'utente decidono; capability native-read-only; result analytical comparison non necessario; root budget 3 waves non speso
simulation persistence: unsaved

## Checkpoints
- C1 needs: D2, D3 -> riscrivere core/ATLAS.md e core/SPOTTER.md con la regola e i tagli -> `wc -c` <= 9000 e check.sh verde; budget: unknown; result: planned; owner: piani docs/plans/2026-09-17-* nei due repo
- C2 needs: D6, D7 -> `spotter setup` su files in cartella Drive (marker, config.json, `— corrente` per area, knowledge.root invariato) -> read-back config e primo `check --audit`; budget: unknown; result: planned, attende go esplicito; owner: unassigned
- C3 needs: D9 -> rilascio (bump manifesti, reinstall, upsert nei repo pinnati) -> core aggiornato letto in una sessione nuova; result: planned, dopo ship autorizzato; owner: unassigned

## Evidence and next check
Fonti: core/ATLAS.md, skills/build/references/tickets.md:15-20, skills/scope/references/intake.md:7, scripts/tracker.sh, scripts/check.sh:29, scripts/core-context.sh:33-60, skills/ship/SKILL.md (regola anti-inferenza di push/PR), skills/improve/SKILL.md:7; spotter core/SPOTTER.md, skills/setup/references/{ontology,tracker}.md, skills/check/references/{audit,week-open}.md, scripts/check.sh:74-98; Linear MCP list_teams/list_projects/list_issues/list_issue_labels/list_cycles 2026-09-16. Assunzione aperta: il connettore Linear su Codex/Cursor (non sondato); se assente, la scelta files/forge regge comunque.

## Out of scope
- Runtime ticket, sqlite, board HTML, secondo backlog: non-goal dichiarati.
- Materializzare l'ontologia in Linear: sostituito da D7 + C2.
- Bump di versione, reinstall, upsert nei repo pinnati: rilascio (ship), non build.
- Nuove skill pubbliche in entrambi i plugin.
