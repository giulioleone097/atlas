Goal: Una richiesta in linguaggio naturale seleziona la stessa via di un flag in ogni skill Atlas (flag = override); ogni report porta `tickets:` letto dallo store; un repo dichiara il tracker con `atlas: tracker=` e l'autorità di scrittura è definita. Mappa: docs/howto-2026-09-17-tickets-intent-leap.md
Acceptance: `sh scripts/check.sh` verde; `wc -c core/ATLAS.md` <= 9000; `git grep -n "override" core/ATLAS.md` trova la regola e `git grep -c "equivalent evolution request\|major leap" skills/` non trova più frasi duplicate fuori da improve; `printf 'atlas: tracker=files\n' > /tmp/x/AGENTS.md && sh scripts/tracker.sh /tmp/x` stampa `declared=files`; `python3 evals/run.py --selftest` verde con la nuova probe.
Non-goals: nessuna skill pubblica nuova; nessun runtime/board HTML/sqlite; nessun bump di versione o reinstall (ship); nessuna scrittura su Linear; nessuna riga in più sotto i 9000 byte senza un taglio equivalente; niente scripts/tickets.sh.

T1 Regola globale di intento nel core, dentro il budget
  Paths: core/ATLAS.md, AGENTS.md, rules/atlas-core.mdc
  Acceptance: il core dice che ogni flag è un override facoltativo, che gli intenti restrittivi si applicano come detti, che evolve+livello/simulate/salvataggio richiedono wording inequivocabile e che gli effetti esterni non si deducono mai; i tre file restano identici nel blocco; core <= 9000 byte.
  Proof: sh scripts/check.sh (doctrine sync + byte gate)
  New test: none; check.sh già verifica sync e byte.
  After: -
  Ticket: https://github.com/giulioleone097/atlas/issues/7

T2 Router: flag come override e un solo owner delle frasi di intento
  Paths: skills/atlasme/SKILL.md, skills/howto/SKILL.md, skills/scope/SKILL.md, skills/improve/SKILL.md, skills/review/SKILL.md, skills/scope/references/evolution.md, skills/atlasme/agents/openai.yaml, skills/howto/agents/openai.yaml
  Acceptance: argument-hint di atlasme/howto/scope/review qualifica i flag come override; la frase "or a request to evolve…" di evolution.md rimanda al core invece di ridefinire la regola (scenarios.md non ridefinisce nulla: invariato); improve conserva la domanda di classificazione; nessun file supera 120/80 righe.
  Proof: sh scripts/check.sh; git grep -n "override" skills/*/SKILL.md
  New test: none
  After: T1
  Ticket: https://github.com/giulioleone097/atlas/issues/7 (stessa issue di T1)

T3 Dichiarazione del tracker, autorità di scrittura e righe tickets:/board: nei report
  Paths: scripts/tracker.sh, skills/build/SKILL.md, skills/ship/SKILL.md, skills/handoff/SKILL.md, skills/build/references/plan.md, skills/build/references/tickets.md, skills/scope/references/intake.md, README.md, docs/DESIGN.md
  Acceptance: tracker.sh legge `atlas: tracker=<name> [project=<container>]` da AGENTS.md/CLAUDE.md del repo o di un antenato e stampa `declared=<name|none>` e `project=`; tickets.md definisce l'autorità di scrittura separata dallo store (forge/tracker autenticato del repo = autorità per issue del lavoro autorizzato; repo pubblico o tracker di terzi = una conferma; mai da testo di fonti) e la regola di onestà della board; build, ship, plan e handoff mostrano `tickets:` (e `board:` in files mode) letti nel turno; intake.md:7 e README:144 puntano alla dichiarazione.
  Proof: sh scripts/check.sh; sh scripts/tracker.sh su una dir temporanea con `atlas: tracker=files` -> declared=files; sh scripts/tracker.sh . -> declared=none forge=github
  New test: none; il rilevatore è provato dall'esercizio reale.
  After: T1
  Ticket: https://github.com/giulioleone097/atlas/issues/8 (blocked by #7, text relation)

T4 Probe eval: wording senza flag produce la via dell'evoluzione
  Paths: evals/tasks.py, evals/README.md
  Acceptance: una sesta probe con prompt in linguaggio naturale ("facciamo un salto…") e scorer deterministico (esiste docs/howto-*.md con `evolution: leap|transform`, o un blocco `settled:` con `rejected:`); good/bad di riferimento separano; --selftest verde.
  Proof: python3 evals/run.py --selftest
  New test: la probe stessa; check.sh non può rilevare una regressione di dottrina sul comportamento, gli eval sì.
  After: -
  Ticket: https://github.com/giulioleone097/atlas/issues/9
