# Chain of Verification

- Проверяемый черновик или утверждение: tests_integration.md

## Запрос на проверку

use TRAINING_PR.diff, tests_integration.md; Improve a weak artifact(tests_integration.md).
1. Draft: черновик рисков.
2. Verify: для каждого риска спроси — где доказательство в diff или правилах?
3. Check: убери утверждения без file:line или источника.
4. Final: верни только подтверждённые риски и проверки.



Draft
- API → Service: No length check for diff; large payloads won’t be rejected with HTTP 413 per API-1.
- Service → LLM: No 10s timeout or controlled error mapping on LLM call per REL-1.
- API ↔ Service: Response schema violates OUT-1; returns {"comment": ...} instead of {summary, risks, checks}.
- Service → LLM: Secrets in diff are sent raw to external LLM; violates SEC-1.

Verify
- API → Service length check:
  - Evidence (code): TRAINING_PR.diff: app/api.py lines 35-37 show endpoint calling review_service.review(payload["diff"]) with no length validation.
  - Rule: API-1 requires rejecting diff > 20,000 chars with HTTP 413 and skipping LLM call.
- Service → LLM timeout/handling:
  - Evidence (code): TRAINING_PR.diff: app/review_service.py lines 20-22 build prompt and call self.llm.generate(prompt) without any timeout or error mapping.
  - Rule: REL-1 requires a 10s timeout and converting errors to a controlled response.
- Response schema mismatch:
  - Evidence (code): TRAINING_PR.diff: app/review_service.py line 22 returns {"comment": answer}; TRAINING_PR.diff: app/api.py lines 35-37 return that directly.
  - Rule: OUT-1 mandates output to contain summary, risks (≤3 with file, line, evidence, risk), and checks.
- Secrets redaction:
  - Evidence (code): TRAINING_PR.diff: app/review_service.py lines 19-21 interpolate raw diff into prompt and send to LLM; no redaction step present.
  - Rule: SEC-1 requires removing tokens/passwords/private keys from diff before sending to external LLM.

Check
- Removed none; all listed risks have explicit evidence with file:line in TRAINING_PR.diff and a referenced rule source.
- Updated evidence references to precise lines in TRAINING_PR.diff rather than vague mentions.

Final
Updated Integration-проверки (confirmed risks and checks only):

| Связь компонентов | Что может сломаться | Как воспроизводим | Ожидаемый результат | Evidence |
|---|---|---|---|---|
| API → Service | Проверка длины диффа и обход LLM | POST /api/reviews с diff длиной > 20000 символов | HTTP 413, вызов LLM не производится (API-1) | TRAINING_PR.diff: app/api.py:35-37 — эндпойнт без проверки длины; правило API-1 |
| Service → LLM | Таймаут и обработка ошибок | Подставить LLM-стаб с задержкой > 10 c или исключением | Ответ ≤ 10 c с контролируемой ошибкой без трассы (REL-1) | TRAINING_PR.diff: app/review_service.py:20-22 — generate без таймаута/обработки; правило REL-1 |
| API ↔ Service | Контракт ответа не соответствует OUT-1 | POST /api/reviews с коротким diff | HTTP 200 с телом {summary, risks[], checks[]} (OUT-1) | TRAINING_PR.diff: app/review_service.py:22 — возвращается {"comment": ...}; app/api.py:35-37 — проксирует как есть; правило OUT-1 |
| Service → LLM | Секреты из diff утекут во внешний LLM | Использовать diff с токеном/ключом; LLM-стаб эхо-ответа | В prompt/ответе секреты отсутствуют или заменены на [REDACTED] (SEC-1) | TRAINING_PR.diff: app/review_service.py:19-21 — сырой diff вставляется в prompt; правило SEC-1 |

Примечания к проверкам:
- Для таймаута и редакции секретов используйте тестовый LLM-стаб: для таймаута — sleep > 10s; для редакции — возвращать принятый prompt, чтобы убедиться, что секреты убраны до вызова generate.



## Вопросы проверки и evidence

| Вопрос | Источник или проверка | Результат |
|---|---|---|
| OUT-1 действительно должен запрещать лишние поля? | Context Pack: OUT-1; сравнить с текущим `review_service.py:17` | Да, контракт фиксирует ровно `summary/risks/checks`; текущий код возвращает `{ "comment": ... }` |
| API-1 — где граница? | Context Pack формулировка + согласование в E2E | 413 только при `> 20000`; `== 20000` валиден |

## Исправленный результат

| Связь компонентов | Что может сломаться | Как воспроизводим | Ожидаемый результат | Evidence |
|---|---|---|---|---|
| API → Service | Проверка длины диффа и обход LLM | POST /api/reviews с diff длиной > 20000 символов | HTTP 413, вызов LLM не производится (API-1) | TRAINING_PR.diff: app/api.py:35-37 — эндпойнт без проверки длины; правило API-1 |
| Service → LLM | Таймаут и обработка ошибок | Подставить LLM-стаб с задержкой > 10 c или исключением | Ответ ≤ 10 c с контролируемой ошибкой без трассы (REL-1) | TRAINING_PR.diff: app/review_service.py:20-22 — generate без таймаута/обработки; правило REL-1 |
| API ↔ Service | Контракт ответа не соответствует OUT-1 | POST /api/reviews с коротким diff | HTTP 200 с телом {summary, risks[], checks[]} (OUT-1) | TRAINING_PR.diff: app/review_service.py:22 — возвращается {"comment": ...}; app/api.py:35-37 — проксирует как есть; правило OUT-1 |
| Service → LLM | Секреты из diff утекут во внешний LLM | Использовать diff с токеном/ключом; LLM-стаб эхо-ответа | В prompt/ответе секреты отсутствуют или заменены на [REDACTED] (SEC-1) | TRAINING_PR.diff: app/review_service.py:19-21 — сырой diff вставляется в prompt; правило SEC-1 |

## Что изменили в исходном артефакте

- Файл и раздел: tests_integration.md
- Изменение: добавлены две новые строки в таблицу
- Что отклонили: -

Скрытые рассуждения модели не сохраняйте; нужны только вопросы, evidence и исправленный результат.
