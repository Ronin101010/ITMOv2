# Integration-проверки

| Связь компонентов | Что может сломаться | Как воспроизводим | Ожидаемый результат | Evidence |
|---|---|---|---|---|
| API → Service | Проверка длины диффа и обход LLM | POST /api/reviews с diff длиной > 20000 символов | HTTP 413, вызов LLM не производится (API-1) | TRAINING_PR.diff: app/api.py:35-37 — эндпойнт без проверки длины; правило API-1 |
| Service → LLM | Таймаут и обработка ошибок | Подставить LLM-стаб с задержкой > 10 c или исключением | Ответ ≤ 10 c с контролируемой ошибкой без трассы (REL-1) | TRAINING_PR.diff: app/review_service.py:20-22 — generate без таймаута/обработки; правило REL-1 |
| API ↔ Service | Контракт ответа не соответствует OUT-1 | POST /api/reviews с коротким diff | HTTP 200 с телом {summary, risks[], checks[]} (OUT-1) | TRAINING_PR.diff: app/review_service.py:22 — возвращается {"comment": ...}; app/api.py:35-37 — проксирует как есть; правило OUT-1 |
| Service → LLM | Секреты из diff утекут во внешний LLM | Использовать diff с токеном/ключом; LLM-стаб эхо-ответа | В prompt/ответе секреты отсутствуют или заменены на [REDACTED] (SEC-1) | TRAINING_PR.diff: app/review_service.py:19-21 — сырой diff вставляется в prompt; правило SEC-1 |

## Как использовали AI

- Строка в [`prompts.md`](prompts.md): P1-02.
- Что проверили и исправили сами: добавили ровно те проверки, которые подтверждают API-1 и REL-1 из Context Pack; избегали не подтверждённых diff гипотез.
