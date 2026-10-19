---
description: "Task list for 001-motor-reembolso implementation"
---

# Tasks: Motor de Cálculo de Reembolso (001-motor-reembolso)

**Input**: Design documents from `/specs/001-motor-reembolso/`

**Prerequisites**: plan.md (required), spec.md (required for rules), research.md, data-model.md, contracts/, quickstart.md

**Tests**: Tests are mandatory for this feature (see plan.md Test Strategy and constitution gate VII).

**Organization**: Tasks are grouped by derived user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Single project: `src/` and `tests/` at repository root
- `src/regras/` — one module per business rule (`RN-001`..`RN-010`)
- `tests/test_regras/` — one test module per rule
- `exemplos/` — sample input JSON

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per implementation plan: `src/`, `src/regras/`, `tests/`, `tests/test_regras/`, and `exemplos/` directories
- [x] T002 Create `requirements-dev.txt` with `pytest` development dependency
- [x] T003 [P] Create `pyproject.toml` with pytest test-discovery configuration (testpaths = `tests/`)
- [x] T004 Review/extend `exemplos/despesas-exemplo.json` to ensure all RN acceptance scenarios are covered

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**?? CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 [P] Create `src/modelos.py` with dataclasses for `Colaborador`, `Periodo`, `Despesa`, `ResultadoDaDespesa`, `Resumo`, and `Alerta`
- [x] T006 [P] Create `src/regras/__init__.py` package file
- [x] T007 [P] Create `src/regras/config.py` with policy limits: `alimentacao` = R$ 60.00, `transporte_urbano` = R$ 80.00, `hospedagem` = R$ 250.00 per diária, travel multiplier = 1.50, and invoice threshold = R$ 100.00
- [x] T008 [P] Create `src/regras/arredondamento.py` implementing RN-010 half-up rounding to two decimal places
- [x] T009 Create `src/motor.py` skeleton and define public API (e.g., `processar(entrada: dict) -> dict`) orchestrating `parse → validate → calculate → emit`
- [x] T010 Create `src/cli.py` with `argparse` subcommand `calcular`, flags `--input` and `--output`, writing errors to `stderr` and exiting non-zero on structural failures
- [x] T011 Create `tests/conftest.py` with shared fixtures for sample expenses, periods, and expected results

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Filtrar e Classificar Despesas Elegíveis (Priority: P1) ?? MVP

**Goal**: Reject or mark expenses that are categorically invalid, out of period, missing invoice above R$ 100.00, duplicated, or refunds; pass only eligible expenses to limit calculation.

**Independent Test**: Run `pytest tests/test_regras/test_categoria.py tests/test_regras/test_periodo.py tests/test_regras/test_nota_fiscal.py tests/test_regras/test_duplicata.py tests/test_regras/test_estorno.py` — all pass.

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T012 [P] [US1] Write contract test for input schema constraints in `tests/test_validacao_entrada.py`
- [x] T013 [P] [US1] Write unit test for RN-008 category validation in `tests/test_regras/test_categoria.py`
- [x] T014 [P] [US1] Write unit test for RN-007 period validation in `tests/test_regras/test_periodo.py`
- [x] T015 [P] [US1] Write unit test for RN-004 invoice requirement in `tests/test_regras/test_nota_fiscal.py`
- [x] T016 [P] [US1] Write unit test for RN-006 duplicate detection in `tests/test_regras/test_duplicata.py`
- [x] T017 [P] [US1] Write unit test for RN-009 refund handling in `tests/test_regras/test_estorno.py`

### Implementation for User Story 1

- [x] T018 [P] [US1] Implement `src/regras/categoria.py` for RN-008: case-insensitive acceptance of `alimentacao`, `transporte_urbano`, `hospedagem`; reject all others
- [x] T019 [P] [US1] Implement `src/regras/periodo.py` for RN-007: reject expenses with `data` outside `periodo.inicio`..`periodo.fim` inclusive
- [x] T020 [P] [US1] Implement `src/regras/nota_fiscal.py` for RN-004: reject expenses with `valor` > R$ 100.00 and `tem_nota_fiscal` = false
- [x] T021 [P] [US1] Implement `src/regras/duplicata.py` for RN-006: detect duplicates by same `data`, `categoria`, `valor`, and `fornecedor`; keep first, reject subsequent
- [x] T022 [P] [US1] Implement `src/regras/estorno.py` for RN-009: mark negative `valor` as `estorno`, non-reimbursable, reducing period total
- [x] T023 [US1] Wire eligibility rules into `src/motor.py` pipeline in the order RN-008 → RN-007 → RN-004 → RN-006 → RN-009

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Aplicar Limites Diários e de Viagem (Priority: P2)

**Goal**: Detect travel from lodging presence and apply daily/category limits to eligible food, transport, and lodging expenses.

**Independent Test**: Run `pytest tests/test_regras/test_viagem.py tests/test_regras/test_limites.py` — all pass.

### Tests for User Story 2

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T024 [P] [US2] Write unit test for RN-005 travel detection in `tests/test_regras/test_viagem.py`
- [x] T025 [P] [US2] Write unit test for RN-001/RN-002/RN-003 daily limits in `tests/test_regras/test_limites.py`
- [x] T026 [P] [US2] Write integration test for travel-expanded limits in `tests/test_regras/test_limites.py`

### Implementation for User Story 2

- [x] T027 [P] [US2] Implement `src/regras/viagem.py` for RN-005: determine national lodging dates and international adjacent dates supported by airport/hotel transport
- [x] T028 [P] [US2] Implement `src/regras/limites.py` for RN-001, RN-002, RN-003:
  - Group alimentacao/transporte_urbano by date, sort by declared value descending (tie preserves input order)
  - Apply daily limit sequentially: full refund while budget remains, first excess gets partial remainder, others rejected
  - Hospedagem limit = R$ 250.00 × inferred diarias (default 1), parsed from `descricao`; multiply limits by 1.50 only on dates identified as travel days
- [x] T029 [US2] Integrate limit application into `src/motor.py` pipeline after eligibility rules and travel detection

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Gerar Resultado Arredondado e Consolidado (Priority: P3)

**Goal**: Produce the final JSON output with rounded per-expense values, period summary totals, and duplicate alerts.

**Independent Test**: Run `python -m reembolso calcular --input exemplos/despesas-exemplo.json --output resultado.json` and validate against `contracts/output-schema.json`.

### Tests for User Story 3

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T030 [P] [US3] Write unit test for RN-010 half-up rounding in `tests/test_regras/test_arredondamento.py`
- [x] T031 [P] [US3] Write integration test for full pipeline in `tests/test_motor.py`
- [x] T032 [P] [US3] Write CLI argument/output test in `tests/test_cli.py`

### Implementation for User Story 3

- [x] T033 [P] [US3] Implement output builder in `src/motor.py`: map each `Despesa` to `ResultadoDaDespesa` with `status` ∈ {aprovado, parcial, rejeitado, estorno} and `motivo`
- [x] T034 [P] [US3] Implement `Resumo` aggregation in `src/motor.py`: `total_declarado`, `total_reembolsavel` minus refunds, `total_nao_reembolsavel`, `total_rejeitado`, `quantidade_despesas`
- [x] T035 [P] [US3] Implement `Alerta` generation in `src/motor.py`: emit `duplicata` alerts listing rejected duplicate IDs
- [x] T036 [US3] Implement JSON read/write and schema validation in `src/cli.py` and `src/motor.py`

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T037 [P] Run quickstart.md validation scenarios against `exemplos/despesas-exemplo.json` and `resultado.json`
- [x] T038 [P] Create `DECISIONS.md` at repository root logging any implementation-time decisions that diverge from plan.md
- [x] T039 [P] Verify every spec.md border case (section 7) has an explicit test
- [x] T040 Run full `pytest` suite and ensure all tests pass
- [x] T041 Verify performance goal: `exemplos/despesas-exemplo.json` processes in < 1s
- [x] T042 [P] Update `specs/001-motor-reembolso/plan.md` or `DECISIONS.md` if any implementation detail changed
- [x] T043 Export this work session to `docs/sessions/` with sequential numbering per project constitution VII
- [x] T044 Update `RELATORIO.md` at repository root with evidence links, decisions, and discernment notes per project constitution VII

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models/services before integration
- Core rule modules before wiring into motor.py
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Rule modules within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
pytest tests/test_regras/test_categoria.py tests/test_regras/test_periodo.py tests/test_regras/test_nota_fiscal.py tests/test_regras/test_duplicata.py tests/test_regras/test_estorno.py -v

# Launch all rule modules for User Story 1 together:
# src/regras/categoria.py
# src/regras/periodo.py
# src/regras/nota_fiscal.py
# src/regras/duplicata.py
# src/regras/estorno.py
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 - eligibility filtering
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Phase 7: Convergence

- [x] T045 CRITICAL Register the RN-005 travel-day change and accepted clarifications in the canonical `DECISIONS.md`, including previous/new behavior, rationale, invalidated artifacts, affected tasks, and cost, per Constitution IV and T038 (missing)
- [x] T046 CRITICAL Add an automated acceptance test proving that a R$ 800.00 lodging expense for two travel diárias is capped at the expanded R$ 750.00 limit per Constitution III and RN-003/RN-005 (missing)
- [x] T047 CRITICAL Provide `RELATORIO.md` at the canonical repository-root location with evidence links, decisions, delegation usage, and a concrete agent-error account, or align all governing artifacts to the justified canonical path, per Constitution V and T044 (missing)
- [x] T048 Make lodging-limit expansion follow the stay dates derived from explicit check-in/checkout even when `despesa.data` differs, and cover the behavior in unit and pipeline tests, per RN-003/RN-005 (partial)
- [x] T049 Align structural validation with the specified behavior of recording a malformed expense error while continuing to process the remaining expenses, including contract and CLI tests, per spec section 3 (contradicts)
- [x] T050 Integrate the `src/modelos.py` entities into validation and result construction or record and propagate the formal decision to retain dictionary-based processing, per plan validation-layer decision and T005/T033 (partial)
