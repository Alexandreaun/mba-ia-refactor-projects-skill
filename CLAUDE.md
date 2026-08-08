# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is the workspace for an MBA challenge ("Criação de Skills — Refatoração Arquitetural Automatizada", see root `README.md` for the full brief in Portuguese). The deliverable is a Claude Code **Skill** named `refactor-arch` that:

1. Analyzes any backend codebase (language/framework/architecture agnostic)
2. Audits it against a catalog of anti-patterns (MVC/SOLID violations, security issues, deprecated APIs), producing a severity-classified report (CRITICAL/HIGH/MEDIUM/LOW)
3. Refactors it into an MVC layout (Models / Views-Routes / Controllers), pausing for user confirmation between the audit and the refactor
4. Validates that the app still boots and all endpoints still respond after refactoring

The skill must be built once and then copied — unmodified in concept, adapted only in invocation path — into all three target projects below, proving it is stack-agnostic.

## Target projects (intentionally flawed — do not "fix casually")

These three projects contain **intentional** code smells, security holes, and architecture violations. They are the fixtures the `refactor-arch` skill is exercised against — do not clean them up ad hoc outside of running the skill's Phase 3, since manual analysis of their *current, broken* state is itself a graded deliverable.

- **`code-smells-project/`** — Python/Flask e-commerce API. Fully unstructured: `app.py` (routes + hardcoded `SECRET_KEY` + a raw `/admin/query` SQL-injection endpoint), `controllers.py`, `models.py` (God Class covering produtos/usuarios/pedidos/itens_pedido), `database.py` (global mutable connection, schema + seed data inlined). Run: `pip install -r requirements.txt && python app.py` → `http://localhost:5000` (SQLite `loja.db`, auto-seeded on first boot).
- **`ecommerce-api-legacy/`** — Node.js/Express LMS API with a checkout flow. `src/app.js` is the entry point, `src/AppManager.js` is a God Class holding the DB connection, route setup, and deeply nested callback-pyramid business logic (checkout, financial reporting via N+1 queries, an endpoint that leaves orphaned rows on user delete), `src/utils.js` holds config/crypto/cache helpers (note `badCrypto` — a deliberately weak hashing stand-in). In-memory SQLite, seeded on boot. Run: `npm install && npm start` → `http://localhost:3000`. Example requests in `api.http`.
- **`task-manager-api/`** — Python/Flask task manager with *partial* layering already in place (`models/`, `routes/`, `services/`, `utils/`) but still containing hardcoded secrets, N+1 query patterns, inconsistent/duplicated validation across routes, and other quality issues — the point is that "already organized" ≠ "architecturally sound". Run: `pip install -r requirements.txt && python seed.py && python app.py` → `http://localhost:5000` (SQLite `tasks.db`; **must run `seed.py` before first boot** or endpoints return empty lists).

## Repository layout for the skill itself

The skill lives at `.claude/skills/refactor-arch/` **inside each target project** (not at the repo root), because the brief requires it be copied project-to-project to prove portability:

```
<project>/.claude/skills/refactor-arch/
├── SKILL.md            # required name/path; the 3-phase prompt (Analysis → Audit → Refactor)
└── <reference files>    # markdown knowledge base, organize freely as long as these 5 areas are covered:
                          #   - project analysis heuristics (language/framework/DB/architecture detection)
                          #   - anti-pattern catalog (>=8 patterns, severities distributed, incl. deprecated-API detection)
                          #   - audit report template
                          #   - target MVC architecture guidelines
                          #   - refactoring playbook (>=8 before/after transformation patterns)
```

Build the skill once in `code-smells-project/.claude/skills/refactor-arch/`, then copy the same directory into `ecommerce-api-legacy/` and `task-manager-api/`.

Audit reports (Phase 2 output) go to `reports/audit-project-{1,2,3}.md` at the repo root, mapping 1→code-smells-project, 2→ecommerce-api-legacy, 3→task-manager-api.

## Working conventions

- **Severity scale** (used consistently across the anti-pattern catalog and audit reports): CRITICAL (architecture/security failures breaking correctness or exposing data — hardcoded creds, SQL injection, God Classes mixing DB+logic+routing), HIGH (strong MVC/SOLID violations — business logic in controllers, tight coupling, mutable global state), MEDIUM (N+1 queries, misused middleware, missing route validation), LOW (naming, magic numbers, readability).
- Phase 2 (Audit) must always pause and ask for explicit user confirmation before Phase 3 (Refactor) touches any file.
- Phase 3 must leave the app in a runnable state — same ports, same endpoint contracts — and validate this by booting the app and hitting the endpoints, not just by inspection.
- When testing a refactor, always run each project's own start command from its README (`python app.py`, `npm start`, or `python seed.py && python app.py`) rather than assuming a shared runner — the three projects have independent, different toolchains and none share dependencies.
