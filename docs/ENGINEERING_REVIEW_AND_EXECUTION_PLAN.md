# Binance Futures Testnet Bot: Engineering Review and Execution Plan

## 1) Confirmed Understanding

This assignment is not just about "placing an order." It is a signal test for backend engineering discipline in a small scope.

We will build a Python 3.11+ CLI application that places `MARKET` and `LIMIT` orders on Binance USDT-M Futures Testnet using direct REST (`requests`) with signed authentication, strict validation, meaningful logging, and custom exception handling.

We will **not** over-engineer. We will keep a clean layered flow:

`cli.py -> validators.py -> orders.py -> client.py -> Binance`

No implementation will be done until you approve this plan.

---

## 2) What The Company Is Actually Testing

1. Can you integrate a real external API correctly (auth, signing, params, timestamps)?
2. Can you design clean layers under constraints?
3. Do you validate inputs before network calls?
4. Do you handle failures predictably (API errors, timeouts, network issues)?
5. Can you log operationally useful events without leaking secrets?
6. Can another engineer run your repo quickly from README alone?
7. Do you show judgment (scope control, readability, practical tradeoffs)?

---

## 3) Common Candidate Mistakes

1. Calling Binance directly from CLI (no service/client layering).
2. Hardcoding credentials or accidentally logging API secret.
3. Not handling timeout/network errors explicitly.
4. No validation for `LIMIT` price or invalid symbols.
5. Treating HTTP 200 as success without checking Binance error payload.
6. No dry-run safety path.
7. README that is incomplete or not reproducible.
8. Too many abstractions for a small project.
9. No tests or low-value tests.
10. Inconsistent or noisy logging.

---

## 4) Top 10% vs Bottom 90%

### Top 10%
1. Clean file responsibilities and data flow.
2. Predictable typed exceptions and helpful user-facing messages.
3. Practical validation (including symbol existence from exchange info).
4. Thoughtful logs: request/response metadata + correlation-friendly timestamps.
5. Minimal but high-value tests using mocks.
6. Concise, production-minded README with exact commands.

### Bottom 90%
1. Monolithic script.
2. Weak/no error handling.
3. Secrets in code or logs.
4. "Works on my machine" setup.
5. Overly generic boilerplate without assignment-specific handling.

---

## 5) Repository Structure Guidance

### Professional (target)
```text
trading_bot/
  bot/
    __init__.py
    config.py
    logging_config.py
    exceptions.py
    validators.py
    client.py
    orders.py
  tests/
    test_validators.py
    test_orders.py
  logs/
  cli.py
  README.md
  requirements.txt
  .env.example
  .gitignore
```

### Over-engineered (avoid)
1. Extra layers like repositories/adapters/factories for this tiny scope.
2. Async architecture, retry frameworks, dependency injection frameworks.
3. Event bus or strategy engine not required by assignment.

### Too simplistic (avoid)
1. Single `main.py` with all logic.
2. No custom exceptions.
3. No tests, no logs directory, weak docs.

---

## 6) Pre-API Validation Rules (must run before network)

1. `symbol` required, uppercase normalized.
2. `side` in `{BUY, SELL}`.
3. `order_type` in `{MARKET, LIMIT}`.
4. `quantity` is numeric and `> 0`.
5. If `LIMIT`, `price` required and `> 0`.
6. If `MARKET`, ignore/prohibit price in CLI behavior definition.
7. Symbol must exist in `exchangeInfo` symbols list.
8. Optional practical check: symbol trading status is tradable in testnet response.

---

## 7) Binance-Specific Edge Cases To Handle

1. Signature mismatch (`-1022` invalid signature).
2. Timestamp drift (`-1021`) when local clock differs from server.
3. Precision/step-size errors (qty/price filter issues).
4. Min notional/min quantity filter failures.
5. Rate limit responses (`429`/`418` behavior and message handling).
6. Temporary service issues (`5xx`).
7. API-level errors wrapped in JSON even when transport succeeded.

---

## 8) Network Failure Cases To Handle

1. Connect timeout.
2. Read timeout.
3. DNS/connection errors.
4. Request exceptions from `requests`.
5. Non-JSON responses where JSON expected.

Handling policy:
1. Raise typed custom exceptions.
2. Log details (without secrets).
3. Print concise failure summary to CLI user.

---

## 9) Logging: Useful vs Forbidden

### Must log
1. Timestamp and log level.
2. Endpoint + HTTP method.
3. Request metadata (symbol, side, type, quantity, price, recvWindow/timestamp if used).
4. Response status code and parsed response summary.
5. Error class + message and failure stage.

### Must NEVER log
1. API secret.
2. Full signature value.
3. Full raw headers if they include API key.
4. `.env` contents.

Allowed: masked API key (e.g., first 4 + last 4 chars).

---

## 10) Exception Architecture

Custom exceptions we should define:
1. `TradingBotError` (base)
2. `ConfigurationError`
3. `ValidationError`
4. `BinanceAPIError` (includes code/message/status)
5. `NetworkError`
6. `AuthenticationError` (signature/timestamp related)
7. `RateLimitError`

Why: clear catch points, cleaner CLI messaging, and testable behavior.

---

## 11) README: What It Must Contain

1. Project overview and scope.
2. Architecture and request flow.
3. Setup instructions (Python version, venv, install).
4. `.env` variables and sample values in `.env.example`.
5. CLI usage and examples for MARKET, LIMIT, BUY, SELL, dry-run.
6. Validation behavior and expected errors.
7. Logging behavior and log file location.
8. Test commands.
9. Design decisions and tradeoffs.
10. Limitations and assumptions.
11. Submission checklist mapping to assignment criteria.

---

## 12) Tests Worth Writing (high value only)

1. Validation success path.
2. Validation failure path (invalid side/type/quantity/price).
3. Market order flow with mocked client response.
4. Limit order flow with mocked client response.
5. Optional: client error mapping test (API/network to custom exceptions).

Do not write low-value tests for argparse internals or trivial getters.

---

## 13) Likely Unnecessary Features (for this assignment)

1. Database persistence.
2. Async/multi-threaded architecture.
3. Advanced order engines (TWAP/Grid/OCO) unless bonus explicitly chosen.
4. Docker/Kubernetes.
5. CI pipelines (nice-to-have, not required for a 60-min test).

---

## 14) Hidden Expectations (not explicitly written)

1. Idempotent-ish behavior and safe dry-run mode.
2. Professional failure messages for reviewers running quickly.
3. No sensitive data exposure.
4. Deterministic structure and predictable outputs.
5. Practical limits and assumptions documented clearly.

---

## 15) Signals of Backend Engineering Maturity

1. Correct boundary separation between layers.
2. Typed error model with meaningful conversion of external failures.
3. Pre-flight validation and safe defaults.
4. Logging as an operations tool, not print spam.
5. Minimal dependencies and clear code organization.
6. Readable naming and straightforward control flow.

---

## 16) Signals That Look AI-Generated (to avoid)

1. Generic abstractions with no clear value.
2. Overly verbose comments stating obvious code.
3. Inconsistent naming and duplicated logic.
4. README that sounds polished but misses runnable details.
5. Boilerplate-heavy tests with weak assertions.

---

## 17) Design Decisions To Explicitly Document

1. Why direct REST over SDK.
2. Why chosen layers and file boundaries.
3. How validation is ordered and why symbol lookup is mandatory.
4. Why custom exception mapping exists.
5. Timeout values and error handling policy.
6. Logging format and redaction policy.
7. Dry-run behavior contract.

---

## 18) Assumptions To Explicitly Document

1. Testnet keys are valid and activated for Futures.
2. User has network access to Binance testnet.
3. Testnet account has sufficient balance/margin.
4. Some fields like average price may not be present immediately for all orders.
5. Exchange rules/filters are accepted as source of truth from API.

---

## 19) Complete Development Roadmap

## PHASE 0: Assignment Analysis
- Objective: Lock scope and acceptance criteria before coding.
- Responsibilities: Parse requirements, define done criteria, reject scope creep.
- Files: `ENGINEERING_REVIEW_AND_EXECUTION_PLAN.md` (this doc).
- Engineering decisions: Direct REST, strict layering, minimal deps.
- Acceptance criteria: Every assignment requirement mapped to a planned module.
- Risks: Missing hidden requirements.
- Review checklist:
1. All mandatory features listed.
2. Evaluation criteria mapped.
3. Bonus scope controlled.

## PHASE 1: Project Setup
- Objective: Create clean, minimal project skeleton.
- Responsibilities: Folder and file scaffolding only.
- Files: root structure + empty module files + `.gitignore`.
- Engineering decisions: Keep package flat under `bot/`.
- Acceptance criteria: Import paths clear; no dead directories.
- Risks: Over-scaffolding.
- Review checklist:
1. Single responsibility per file is enforceable.
2. Logs and tests folders present.
3. No extra framework baggage.

## PHASE 2: Configuration Design
- Objective: Centralized environment/config loading.
- Responsibilities: Load API key/secret/base URL/timeout from env.
- Files: `bot/config.py`, `.env.example`.
- Engineering decisions: Fail fast on missing required secrets.
- Acceptance criteria: Config loads once and is reusable by layers.
- Risks: Accidental defaulting to invalid secrets.
- Review checklist:
1. No hardcoded secrets.
2. Helpful errors for missing env vars.
3. Timeout configurable.

## PHASE 3: Logging Architecture
- Objective: Structured, safe logging to file (+ optional console).
- Responsibilities: Configure formatter/handlers/redaction utility.
- Files: `bot/logging_config.py`, `logs/` usage.
- Engineering decisions: One logger namespace for app modules.
- Acceptance criteria: Requests, responses, and errors logged with timestamps.
- Risks: Secret leakage; noisy logs.
- Review checklist:
1. API secret never logged.
2. API key masked if logged.
3. Log lines useful and concise.

## PHASE 4: Validation Architecture
- Objective: Deterministic validation before API calls.
- Responsibilities: Validate symbol/side/type/quantity/price rules.
- Files: `bot/validators.py`.
- Engineering decisions: Normalize user input to uppercase enums/strings.
- Acceptance criteria: Invalid input never reaches order placement.
- Risks: Over-validating with stale assumptions.
- Review checklist:
1. LIMIT requires price > 0.
2. MARKET path valid without price.
3. Clear validation error messages.

## PHASE 5: Exception Architecture
- Objective: Consistent error taxonomy across layers.
- Responsibilities: Define custom exceptions and conversion strategy.
- Files: `bot/exceptions.py`.
- Engineering decisions: Keep exceptions domain-specific and minimal.
- Acceptance criteria: CLI can map exception types to clear output.
- Risks: Too many exception classes.
- Review checklist:
1. Base + specialized exceptions defined.
2. External errors mapped deterministically.
3. Exception messages actionable.

## PHASE 6: Binance Authentication
- Objective: Correct HMAC SHA256 signature workflow.
- Responsibilities: Build signed query using timestamp and params.
- Files: `bot/client.py`.
- Engineering decisions: Sign only query string; attach API key header.
- Acceptance criteria: Auth fields generated correctly for signed endpoints.
- Risks: Signature or timestamp drift issues.
- Review checklist:
1. Timestamp included.
2. Signature derived from exact query string.
3. Header `X-MBX-APIKEY` applied.

## PHASE 7: HTTP Client Design
- Objective: Reliable REST wrapper for Binance endpoints.
- Responsibilities: Implement `get_server_time`, `get_exchange_info`, `place_order`.
- Files: `bot/client.py`.
- Engineering decisions: Centralized request executor with timeout + error mapping.
- Acceptance criteria: Clean responses or typed exceptions only.
- Risks: Incomplete handling of non-200/non-JSON cases.
- Review checklist:
1. All calls use timeout.
2. API and network failures separated.
3. Request/response metadata logged.

## PHASE 8: Order Service Layer
- Objective: Orchestrate validate -> prepare -> submit -> normalize.
- Responsibilities: Business flow and response shaping for CLI.
- Files: `bot/orders.py`.
- Engineering decisions: Service returns normalized dict/model for output.
- Acceptance criteria: MARKET and LIMIT both routed correctly.
- Risks: Hidden coupling with CLI argument formats.
- Review checklist:
1. Service depends on client abstraction, not CLI.
2. Validation executed before submit.
3. Output includes required fields (`orderId`, `status`, `executedQty`, `avgPrice` if present).

## PHASE 9: CLI Design
- Objective: User-friendly command execution.
- Responsibilities: Parse args, call validator/service flow, print concise summaries.
- Files: `cli.py`.
- Engineering decisions: `argparse` subcommands or flags (simple single-command preferred).
- Acceptance criteria: `--help` is clear; error messages readable.
- Risks: CLI bypassing validation rules.
- Review checklist:
1. Inputs map cleanly to service.
2. No direct Binance API calls from CLI.
3. Success/failure output aligns with assignment.

## PHASE 10: Dry-Run Mode
- Objective: Safe preview mode for reviewers.
- Responsibilities: Validate and print payload without order submission.
- Files: `cli.py`, `bot/orders.py`.
- Engineering decisions: Service supports explicit `dry_run=True` branch.
- Acceptance criteria: No network POST when dry-run flag is enabled.
- Risks: Accidentally placing order in dry-run branch.
- Review checklist:
1. Validation still executes.
2. Output clearly states no order sent.
3. Logs mark dry-run explicitly.

## PHASE 11: Testing
- Objective: Cover high-risk logic with minimal, strong tests.
- Responsibilities: Validation and service flow tests with mocks.
- Files: `tests/test_validators.py`, `tests/test_orders.py`.
- Engineering decisions: Mock client responses to avoid live dependency.
- Acceptance criteria: Core behavior validated locally and repeatably.
- Risks: Over-mocking hides integration issues.
- Review checklist:
1. Success + failure validation tests.
2. MARKET and LIMIT service tests.
3. Error-path assertions meaningful.

## PHASE 12: Documentation
- Objective: Make reviewer setup and execution frictionless.
- Responsibilities: Write concise but complete README.
- Files: `README.md`, `requirements.txt`, `.env.example`.
- Engineering decisions: Include exact commands and expected output sections.
- Acceptance criteria: Fresh machine can run from docs only.
- Risks: Mismatch between README and real CLI behavior.
- Review checklist:
1. Setup and run steps exact.
2. Env vars documented.
3. Logging/testing/design decisions included.

## PHASE 13: Final Review
- Objective: Submission quality gate.
- Responsibilities: Requirement traceability + polish pass.
- Files: Whole repository + logs samples.
- Engineering decisions: No extra features beyond rubric.
- Acceptance criteria: Every must-have checkbox satisfied.
- Risks: Last-minute regressions.
- Review checklist:
1. One successful MARKET log captured.
2. One successful LIMIT log captured.
3. No secrets in code/logs.
4. Imports clean; no dead code.
5. Reviewer can evaluate in <10 minutes.

---

## 20) Implementation Guardrails (During Build)

1. Build phase-by-phase; no big-bang coding.
2. Keep functions small and explicit.
3. Add only dependencies already approved.
4. Prefer clarity in names and error messages.
5. Stop and review after each major phase before moving forward.

---

## 21) Ready-For-Build Definition

We start implementation only after you approve:
1. Architecture and file boundaries.
2. Exception taxonomy.
3. Validation rules.
4. Logging redaction policy.
5. Test scope.
6. README outline and constraints.

