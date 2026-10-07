# Skill Confirmation: test-driven-development

Цель
- Показать, что skill TDD применён при реализации фичи B.

Применение (Red → Green → Refactor)
- Red: добавлен тест `test_capacity_limit` в `test_service.py`, ожидающий `RuntimeError("capacity exceeded")` при попытке добавить 101-го уникального подписчика. Запуск `sh scripts/check.sh` дал FAIL только на этом тесте (остальные — PASS).
- Green: изменён `service.py`: введён `MAX_SUBSCRIBERS = 100`, проверка лимита перед добавлением нового уникального имени, дубликаты не считают лимит. Повторный запуск `sh scripts/check.sh` — все тесты PASS.
- Refactor/Verify: убедились, что сценарии A сохранены (пустое имя/слишком длинное имя/ошибка зависимости), а дубликаты не расходуют лимит. Структура кода минимальна, без лишних зависимостей.

Ссылки
- Skill reference: `.opencode/skills/test-driven-development/SKILL.md`, `writing-good-tests.md`.
- Тесты: `practices/practice_03/lab/demo/test_service.py` (блок `test_capacity_limit`).
- Реализация: `practices/practice_03/lab/demo/service.py` (константа `MAX_SUBSCRIBERS`, проверка перед `subscribers.add`).

Результат
- `sh scripts/check.sh` — OK, все тесты проходят. Фича B реализована через TDD, сценарии A не сломаны.
