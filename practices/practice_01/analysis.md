# Анализ процесса: AS IS и TO BE

## AS IS

Событие: пользователь (ревьюер) отправляет `POST /api/reviews` с телом `payload: dict`.

Последовательность по фактам diff:

- `app/api.py:9` принимает `payload: dict`, без схемы и валидации, достаёт `payload["diff"]` и передаёт в сервис.
- `app/review_service.py:15` формирует строковый промпт, включающий сырой `diff` без маскирования секретов (SEC-1 нарушен).
- `app/review_service.py:16` вызывает `self.llm.generate(prompt)` без таймаута и обработки ошибок (REL-1 нарушен).
- `app/review_service.py:17` возвращает `{"comment": answer}`; `app/api.py:9` транслирует наружу этот же формат. Требуемые `summary/risks/checks` отсутствуют (OUT-1 нарушен).

Обязательная связка: `api.py:9 → review_service.py:15–16 → LLM`.

```mermaid
flowchart LR
    C[Client] -->|POST /api/reviews| A[API app/api.py:9]
    A -->|payload["diff"]| S[Service review_service.py:15]
    S -->|prompt with raw diff| L[LLM generate() review_service.py:16]
    L --> R[{"comment": answer}\nreview_service.py:17]
    R --> O[API returns as-is\napp/api.py:9]
```

Узкие места и риски:

- Нет проверки длины входа > 20 000 символов на уровне API (API-1).
- Нет таймаута 10 с и контролируемой обработки ошибок LLM (REL-1).
- Формат ответа не соответствует OUT-1.
- Тело запроса без схемы, возможен `KeyError` и 5xx на невалидном входе.

## TO BE

Минимально необходимый процесс с соблюдением правил репозитория:

1. API проверяет тело запроса на наличие строки `diff`; невалидный вход → 400/422.
2. API проверяет длину `diff`; при > 20 000 символов возвращает 413 (API-1) без вызова LLM.
3. Сервис перед вызовом LLM маскирует секреты в `diff` (SEC-1).
4. Вызов LLM выполняется с таймаутом 10 секунд и контролируемой обработкой ошибок (REL-1).
5. Ответ приводится к контракту OUT-1: `summary`, `risks` (≤ 3, с `file`, `line`, `evidence`, `risk`), `checks`.
6. Пользователь просматривает результат и принимает решение (SCOPE-1: сервис советует, не действует).

```mermaid
flowchart LR
    C[Client] -->|POST /api/reviews| A[API validate & limit\napp/api.py]
    A -->|<= 20k| P[Preprocess: mask secrets\nSEC-1]
    P -->|prompt| L[LLM call with timeout\nREL-1]
    L --> O[Shape to OUT-1]
    O --> U[User review\nSCOPE-1]
```

## Разница

| Что меняется | AS IS | TO BE | Как проверим изменение |
|---|---|---|---|
| Валидация тела | `payload: dict`, `payload["diff"]` без схемы → возможен 5xx | Схема/валидация, невалидный вход → 4xx | E2E негативный: без `diff` → 4xx |
| Ограничение длины | Нет проверки длины (api.py:9) | При > 20 000 символов → HTTP 413 (API-1) | Integration: diff > 20 000 → 413 |
| Маскирование секретов | Сырой diff в промпте (review_service.py:15) | Маскирование токенов/паролей до вызова LLM (SEC-1) | Unit: `token=TEST_SECRET` → `[REDACTED]` в промпте |
| Таймаут и ошибки LLM | Нет таймаута/обработки (review_service.py:16) | Таймаут 10 с и контролируемый ответ (REL-1) | Integration: LLM-стаб со sleep > 10 с → контролируемый ответ ≤ 10 с |
| Формат ответа | `{ "comment": ... }` (review_service.py:17 → api.py:9) | `summary/risks/checks` (OUT-1) | E2E позитивный: структура ответа соответствует OUT-1 |

## Как использовали AI

- Для чего: описать текущее и целевое состояние процесса на основании одного diff и подтверждённых правил.
- Тип промпта: master prompt.
- Строка в [`prompts.md`](prompts.md): P1-02.
- Что проверили и исправили сами: включили обязательные привязки к строкам diff в AS IS (`api.py:9 → review_service.py:15–16 → LLM`) и добавили шаг маскирования секретов по SEC-1 в TO BE; увязали проверки с метриками из `problem.md`.
