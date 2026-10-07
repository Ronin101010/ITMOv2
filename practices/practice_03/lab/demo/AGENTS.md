# AGENTS.md

Краткие правила для агента по работе с этим проектом (Notify Mini, demo из практики 3).

Что это за проект
- Учебный сервис подписки с простой функцией `subscribe(name)` в `service.py` и тестами `test_service.py`.

Контракт требований и проверки
- Контракт требований: `docs/style-guide.md` и этот файл.
- Пример теста: `test_service.py`.
- Команда проверки: `sh scripts/check.sh` (внутри — `make test`).

Ограничения
- Не менять контракт и runner без отдельного поручения.
- Для фичи A сначала показать падающий тест, затем исправление. Показать diff и выполненные команды.
- Поддерживать читаемость и простоту (см. style guide).

Что искать/читать перед началом
- `docs/style-guide.md` — 3–5 правил и один пример.
- `test_service.py` — существующие и новые тесты для A/B.

Навыки и подключения
- Skill: test-driven-development (.opencode/skills/test-driven-development/), читать writing-good-tests.md и применять к A.
- MCP: Context7 добавлен в `opencode.json` для документации/примеров.

Как проверять результат
- Запуск `sh scripts/check.sh` должен возвращать PASS после исправления.
- Hook `.opencode/plugins/check-after-edit.js` запускает проверку после правки и возвращает результат агенту.
