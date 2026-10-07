# Handoff: Practice 4 (Notify Mini)

Состояние (на момент handoff)
- База: проект Notify Mini (practices/practice_03/lab/demo).
- Фича A: входная валидация — пустые имена и имена >255 символов отклоняются (`ValueError`).
- Фича B: ограничение вместимости подписчиков — при 100 уникальных подписчиках попытка добавить 101-го даёт `RuntimeError("capacity exceeded")`; дубликаты не расходуют лимит. Обработка отказа зависимости (демо-флаг `fail_dependency`) выдаёт понятную ошибку.

Источники и артефакты
- Код: `service.py`.
- Тесты: `test_service.py` (включая тесты A и B).
- Правила: `AGENTS.md`, `docs/style-guide.md`.
- Skill: `.opencode/skills/test-driven-development/` (SKILL.md, writing-good-tests.md).
- Hook: `.opencode/plugins/check-after-edit.js` (запускает проверки после правок).
- MCP: `opencode.json` (подключён context7).

Команда проверки
- `sh scripts/check.sh` → `make test` → ожидаем PASS.

Ограничения и заметки
- Не менять контракт и runner без поручения.
- Worktree для B: изменения B делались в отдельной рабочей копии; объединение — через `git merge --ff-only` после приёмки.

Следующие шаги для новой сессии
1. Прочитать `AGENTS.md` и этот `docs/HANDOFF.md`.
2. Запустить `sh scripts/check.sh`.
3. Ничего не менять до получения следующего поручения.
