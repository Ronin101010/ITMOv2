# RAG

- Вопрос к источникам: где именно в diff подтверждаются правила SEC-1, API-1, REL-1, OUT-1 для артефактов Практики 1?

## Разрешённые источники

| Файл или документ | Зачем нужен | Какой фрагмент используем |
|---|---|---|
| `practices/practice_01/TRAINING_PR.diff` | Точное evidence по строкам | `app/review_service.py:15–17`, `app/api.py:9` |
| `practices/practice_01/context.md` | Формулировки правил (SEC-1, API-1, REL-1, OUT-1) | Раздел «Факты и правила» |

## Запрос

Выполни целевой поиск evidence для правил SEC-1, API-1, REL-1, OUT-1, используя только разрешённые источники. Верни таблицу Rule → Evidence c точными ссылками на строки diff.

## Ответ со ссылками на источники

| Rule | Evidence |
|---|---|
| SEC-1 | TRAINING_PR.diff: app/review_service.py:15 — в prompt попадает сырой diff без маскирования |
| API-1 | TRAINING_PR.diff: app/api.py:9 — нет проверки длины, прямой проксирующий вызов |
| REL-1 | TRAINING_PR.diff: app/review_service.py:16 — `self.llm.generate(prompt)` без таймаута/обработки |
| OUT-1 | TRAINING_PR.diff: app/review_service.py:17 → api.py:9 — наружу отдаётся `{"comment": ...}` вместо `summary/risks/checks` |

## Что изменили в исходном артефакте

- Файл и раздел: `practices/practice_01/context.md` — «Факты и правила» (добавлен блок Rule → Evidence)
- Изменение: добавили таблицу соответствия правил и ссылок на строки TRAINING_PR.diff
- Как проверили ссылки: открыли diff и сверили наличие строк; сопоставили с уже указанными в P1 артефактами ссылками
- Что отклонили как неподтверждённое: любые новые правила (auth, rate limiting, snake_case, i18n) — нет источников в diff/Context Pack
