# R.C.T.F.

- **Role:** помощник ревьюера backend PR.
- **Context:** diff + правила репозитория.
- **Task:** summary; до 3 рисков с file:line; проверки.
- **Format:** summary / risks / checks.
- **Boundaries:** не approve, не merge, не меняй код. Если данных мало — задай вопрос.
## Полный запрос
Role: помощник ревьюера backend PR.
Context: TRAINING_PR.diff, tests_unit.md.
Task: Improve a weak artifact(tests_unit.md); summary; до 3 рисков с file:line; проверки.
Format: summary / risks / checks.
Boundaries: не approve, не merge, не меняй код. Если данных мало — задай вопрос.

## Что получили
summary
- PR adds a minimal review flow: ReviewService.review builds a prompt with the raw diff and calls LLM.generate, returning {"comment": answer}. FastAPI adds POST /api/reviews that forwards payload["diff"] to the service; GET /health remains.
- The implementation ignores repository rules from the Context Pack: no secret redaction (SEC-1), no diff-length guard (API-1), no timeout/error handling for LLM (REL-1), and the response shape does not match OUT-1.

risks
- app/review_service.py:20 — evidence: prompt = f"Review this pull request and find problems:\n{diff}" — risk: Secrets in the diff can be exfiltrated to the external LLM, violating SEC-1; repository requires masking to [REDACTED] before any LLM call.
- app/review_service.py:22 — evidence: return {"comment": answer} — risk: Response format violates OUT-1; clients expect {summary, risks (≤3 with file,line,evidence,risk), checks}, so downstream consumers may break.
- app/api.py:9 — evidence: def create_review(payload: dict) -> dict[str, str]: ... return review_service.review(payload["diff"]) — risk: No 20 000-char size check (API-1). Oversized diffs won’t return HTTP 413 and may overload the LLM call or service.

checks
- Improved unit test plan (replacement for tests_unit.md):

| Требование или правило | Что проверяем изолированно | Вход | Ожидаемый результат | Evidence |
|---|---|---|---|---|
| SEC-1 | Маскирование секретов перед вызовом LLM | diff содержит token=TEST_SECRET и password=foo | В промпте вместо секретов — [REDACTED]; LLM получает замаскированные значения | review_service.py:20 — сырой diff включается в промпт |
| API-1 | Ограничение длины diff и HTTP 413 | diff длиной 20001+ символ | POST /api/reviews возвращает 413 и не вызывает LLM | api.py:9–10 — отсутствует проверка длины |
| OUT-1 | Структура ответа сервиса | Произвольный валидный diff | Ответ имеет поля summary, risks (≤3, с file,line,evidence,risk), checks; лишних полей нет | review_service.py:22 — сейчас {"comment": ...}; api.py:9–10 — проксирует как есть |

If you want, I can turn this into concrete pytest tests with a fake LLM and FastAPI TestClient once you confirm the expected error payload for 413 and the exact “controlled response” schema on LLM timeout (REL-1).

## Что изменили в исходном артефакте

- Файл и раздел: tests_unit.md
- Изменение: замена таблицы на SEC-1/API-1/OUT-1 с явной структурой ожиданий
- Как проверили: сопоставили evidence с реальными данными и проверили необходимость проверок
- Что отклонили: лишний четвёртый риск
