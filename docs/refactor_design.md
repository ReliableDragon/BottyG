# BottyG Refactor Design

## Goal
Reduce technical debt in the bot runtime while preserving current user-visible behavior.

## Findings

### 1) Event-loop blocking I/O in `on_message` (High)
- File: `botty_g.py`
- Firestore reads/writes run synchronously inside async handlers.
- Risk: message handling latency and throughput degradation under load.

### 2) Single-file "god module" architecture (High)
- File: `botty_g.py`
- Command handling, infra setup, storage logic, constants, and bot lifecycle are all co-located.
- Risk: high coupling, harder reviews, and regression-prone feature additions.

### 3) Command routing overlap risk (High)
- File: `botty_g.py`
- Routing is implemented with many `startswith` checks.
- Risk: collisions like `!rocket_count` accidentally matching `!rocket`.

### 4) Inefficient count reads for `!counts` (Medium)
- File: `botty_g.py`
- `!counts` currently reads each counter separately.
- Risk: unnecessary Firestore reads and added latency.

### 5) Hardcoded config/IDs in code (Medium)
- Files: `botty_g.py`, `reactions.py`
- Project ID, guild IDs, and special user IDs are embedded in source.
- Risk: brittle deployments and environment-specific drift.

### 6) Import-time side effects (Medium)
- File: `botty_g.py`
- Logging handlers are configured on import.
- Risk: test fragility and duplicate handler bugs in alternate entrypoints.

### 7) Legacy Firebase script tests still in repo (Low)
- Files: `firebase_test.py`, `firebase_test_local.py`
- Script-style files mutate real data and are not in pytest flow.
- Risk: accidental data writes and unclear test boundaries.

### 8) Content/constants mixed with runtime logic (Low)
- File: `botty_g.py`
- Quotes, reaction URLs, and command text are in the main runtime module.
- Risk: poor readability and drift between help text and supported commands.

## Refactor Plan

### Phase 1: Command Routing and Storage Efficiency
- Introduce explicit command registry with exact command token parsing.
- Add single-read counter fetch for `!counts`.
- Keep behavior identical.

### Phase 2: Non-blocking Persistence
- Move Firestore operations behind async-safe boundary (`asyncio.to_thread` or queue worker).
- Add bounded error logging and retries where appropriate.

### Phase 3: Module Decomposition
- Split `botty_g.py` into:
  - `bot/app.py` (client + orchestration)
  - `bot/commands.py` (command handlers)
  - `bot/services/mentions_store.py`
  - `bot/services/secrets.py`
  - `bot/config.py`
  - `bot/content.py`

### Phase 4: Configuration Externalization
- Move IDs/project settings to env-driven config with defaults.
- Validate config at startup.

### Phase 5: Test Cleanup and Hardening
- Retire or relocate legacy Firebase script tests.
- Add emulator-backed integration tests for Firestore paths.
- Ensure help text is generated from command registry to prevent drift.

## Progress Tracker

- [x] Findings documented
- [x] Phase 1: Command registry and single-read counts
- [x] Phase 2: Non-blocking persistence path
- [x] Phase 3: Module decomposition
- [x] Phase 4: Config externalization
- [x] Phase 5: Test cleanup and Firestore integration tests

### Phase 1 Delivered
- Switched command handling to token-based routing for exact command matching.
- Added dedicated command handlers (`_handle_counter_commands`, `_handle_simple_commands`).
- Added `get_all_keyword_mention_counts()` for single-read counter retrieval.
- Updated `!counts` to use one Firestore read.

### Phase 2 Delivered
- Added async wrappers around Firestore interactions:
  - `increment_keyword_mentions_async(...)`
  - `get_all_keyword_mention_counts_async(...)`
- Moved message-path Firestore reads/writes to `asyncio.to_thread(...)`.
- Updated command/count handling to use async counter reads.

### Phase 3 Delivered
- Added `bot/` package and split concerns into modules:
  - `bot/config.py`
  - `bot/content.py`
  - `bot/services/secrets.py`
  - `bot/services/mentions_store.py`
  - `bot/handlers/commands.py`
- Reworked `botty_g.py` into an orchestration layer using the new modules.
- Preserved existing external API surface in `botty_g.py` to keep tests stable.

### Phase 4 Delivered
- Externalized runtime config to environment-backed settings (with defaults):
  - `BOTTYG_PROJECT_ID`
  - `BOTTYG_SECRET_ID`
  - `BOTTYG_MENTIONS_COLLECTION`
  - `BOTTYG_MENTIONS_DOC`
  - `BOTTYG_DEMO_SERVER_ID`
  - `BOTTYG_ATOMIC_FRONTIER_ID`
  - `BOTTYG_MILD_USER_ID`
- Added startup config validation via `validate_runtime_config()`.
- Routed special-user reaction logic through config (`MILD_USER_ID`) instead of hardcoded literal.

### Phase 5 Delivered
- Removed legacy script-style Firebase test files from project root.
- Added emulator-gated Firestore pytest integration test:
  - `tests/test_firestore_integration.py`
- Added pytest integration marker configuration in `pytest.ini`.
- Documented integration test execution in `README.md`.

## Success Criteria

- Bot response behavior remains unchanged for existing commands.
- `!counts` and `!*_count` continue to work with lower read overhead.
- No synchronous Firestore calls in async message handling path.
- New structure supports adding commands without `startswith` collision risk.
