# Журнал экспериментов Практики 2

- Выбранный слабый артефакт Практики 1: `tests_e2e.md`
- Что в нём нужно улучшить: сделать ожидаемые результаты проверяемыми и однозначными (явная структура OUT-1, проверка ограничения ≤3 рисков, граничный случай длины 20000)
- Как поймём, что изменение полезно: E2E-таблица содержит точные ожидаемые поля, включает граничный случай 20000 и исключает нефактические требования; интеграции и юниты согласованы с E2E



| Техника | Файл эксперимента | Изменённый файл Практики 1 | Конкретное изменение | Проверка | Что отклонили |
|---|---|---|---|---|---|
| Few-shot | [`few_shot/experiment.md`](few_shot/experiment.md) | tests_e2e.md | уточнены ожидаемые поля OUT-1 и добавлен граничный сценарий 20000 | сравнение с OUT-1 и Context Pack | требования вне scope (auth, rate limiting) |
| R.C.T.F. | [`rctf/experiment.md`](rctf/experiment.md) | tests_unit.md | таблица unit-проверок замещена на SEC-1/API-1/OUT-1 | сопоставление evidence с реальностью | лишний четвёртый риск |
| Chain of Verification | [`chain_of_verification/experiment.md`](chain_of_verification/experiment.md) | tests_integration.md | добавлены проверки REL-1 и OUT-1 | наличие evidence file:line | непроверяемые утверждения без источника |
| Tree of Thoughts | [`tree_of_thoughts/experiment.md`](tree_of_thoughts/experiment.md) | adr.md | уточнили место шейпинга OUT-1 (в сервисе) и альтернативы | связность ADR с тестами | отдельный Presenter-слой на этом этапе |
| RAG | [`rag/experiment.md`](rag/experiment.md) | context.md | добавлена таблица Rule → Evidence из TRAINING_PR.diff | ссылки на строки diff | новые правила без подтверждения |
| ReAct | [`react/experiment.md`](react/experiment.md) | product_management.md | добавлен boundary-сценарий (len(diff) == 20000) | запуск по чек-листу AC | тесты логирования OBS-1 (непрактично в E2E)

## Независимое ревью

| Замечание другой команды | Где исправили | Evidence |
|---|---|---|
| Двусмысленность | tests_e2e.md — уточнили, что len(diff) == 20000 считается валидным (413 — только > 20000) | Context Pack: API-1 формулировка, P1 материалы |
| Непроверяемое требование | tests_e2e.md — убрали расплывчатое «ответ должен быть полезным», заменили на явную структуру JSON | OUT-1 в Context Pack |
| Пропущенный риск или источник | context.md — добавили таблицу Rule → Evidence со ссылками на строки TRAINING_PR.diff | TRAINING_PR.diff: app/review_service.py:15–17; app/api.py:9 |
