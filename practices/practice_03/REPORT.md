# Отчёт: локальные модели

Отчёт ведёт OpenCode по фактическим результатам команд и вашим сообщениям в чате. Ниже зафиксированы окружение, конфигурация моделей, локальные эксперименты через API Ollama и проверка локальной модели в OpenCode на учебном проекте. Выводы отмечены по фактам без оценок.

## Окружение

ОС / CPU / GPU / RAM:
- Linux (WSL2) 6.18.40.1-microsoft-standard-WSL2, x86_64
- CPU: не собирали подробно (uname подтверждён)
- GPU: NVIDIA (offload активен по ollama ps)
- RAM/VRAM: не измеряли отдельно в этом запуске

Версии инструментов:
- Ollama: 0.34.4
- OpenCode: 1.18.31
- Python: 3.14.4
- curl: 8.18.0
- make: 4.4.1

Локальные веса и модели:
- Базовая модель: qwen3.5:4b (gguf, семейство qwen35, Q4_K_M)
- Локальный image через Modelfile: itmo-local (FROM qwen3.5:4b)
- Локальный image для OpenCode-агента: itmo-agent (PARAMETER num_ctx 65536)

Подтверждения API Ollama:
- GET /api/tags: ok, присутствуют qwen3.5:4b (digest sha256:2a654d98e6fb...) и itmo-local (digest sha256:721e9669...)
- ollama show qwen3.5:4b: контекст 262144, quantization Q4_K_M, capabilities tools/thinking
- ollama show itmo-local: num_ctx 4096 и SYSTEM из Modelfile применены

## Воспроизведение лабораторного демо

Проект demo проверен: make install && make test — OK (3 теста, все пройдены).

Команды локального API и эксперимент baseline/system:
- ollama create itmo-local -f Modelfile — success
- ollama run itmo-local "Объясни разницу между моделью и сервером двумя предложениями" — ответ получен
- python3 experiment.py --mode baseline --output results/baseline.json — OK
- python3 experiment.py --mode system --output results/system.json — OK

Результаты (сводка по содержанию ответов и метрикам):
- baseline: модель ответила развёрнуто, без придумывания CI-конфигурации; wall≈7.15s, decode≈37 tok/s
- system (с SYSTEM из system.txt): короткий ответ «В предоставленных материалах нет ответа.»; wall≈1.97s, decode≈51.9 tok/s

Сравнение temperature/seed (6 конфигураций, по 3 прогретых повтора каждая):
- temperature 0.8, seeds 42/43/44: во всех повторах модель признала отсутствие данных о CI; метрики записаны в results/hot*.json
- temperature 0.2, seeds 42/43/44: аналогично, ответы корректно указывают на отсутствие сведений; метрики в results/cold*.json
Наблюдение: повышение temperature в данной задаче не привело к выдумыванию CI.

Метрики скорости (по файлам результатов):
- Для каждого запуска записаны wall_seconds, load_seconds, total_seconds, decode_tokens_per_second.
- Холодный старт отдельно не выделяли вручную; прогрев обеспечен повторными запусками. TTFT не измеряется скриптом.

## Локальная модель в OpenCode

Подготовка образа для агента:
- ollama create itmo-agent -f Modelfile.agent — OK
- ollama show itmo-agent: num_ctx 65536 применён
- ollama run itmo-agent "Ответь: READY" — ответ READY
- ollama ps: процесс itmo-agent с CONTEXT 65536, 100% GPU

Запуск OpenCode на демо-проекте с агентом local-guide (чтение только):
- opencode run ... > results/read-check.jsonl — OK
- Подтверждён фактический вызов инструмента read c путём demo/README.md
- Ответ помощника: команда тестирования make test, file:line = README.md:6

Пять вопросов из lab/QUESTIONS.md (каждый отдельной сессией):
1) Как запустить тесты? Ответ: make test (README.md:6). Инструменты: read ✓
2) Пустое имя подписчика? Ответ: ValueError("empty name") (service.py:5–6; test_service.py:14–15). read ✓
3) Где реализован unsubscribe? Ответ: отсутствует в коде (service.py:1–9; тестов нет). glob+read ✓
4) Какая CI-система? Ответ: сведений нет (README.md:6 указывает только make test). read ✓
5) Сохраняются ли подписки после перезапуска? Ответ: нет, хранение в памяти процесса (service.py:1 — subscribers = set()). read ✓

## Выводы по задачам практики

- Локальный сервер Ollama и выбранная модель qwen3.5:4b работают стабильно; SYSTEM в Modelfile/system.txt влияет на стиль и строгость ответа.
- Во всех вариациях temperature и seed модель корректно отказалась придумывать CI и следовала ограничению контекста.
- Интеграция с OpenCode через локальный провайдер ollama/itmo-agent подтверждена: инструменты read/glob/grep доступны и фактически вызывались; ответы соответствуют содержимому файлов.

Невыполненные или не измеренные пункты:
- Точное измерение RAM/VRAM и TTFT не выполнялось.
- Сравнение альтернативных семейств/квантизаций не проводилось (необязательное в рамках практики).

## Домашняя работа: локальный помощник по своему проекту (A/B)

Проект: учебный репозиторий демо (lab/demo) из практик 1–2.
Ограничения: тестовая конфигурация OpenCode с правами только на чтение; локальная модель через провайдера ollama (itmo-agent).

Фактор A/B: system prompt агента.
- A: repo-system.txt (исходный)
- B: repo-system-b.txt (усиленные инструкции: цитата строк file:line и явный отказ при отсутствии сведений)

Одинаковые условия для A и B:
- Модель: ollama/itmo-agent (qwen3.5:4b, num_ctx 65536)
- Провайдер: локальный Ollama (baseURL http://localhost:11434/v1)
- Права: только read/glob/grep
- Вопросы: пять из lab/QUESTIONS.md
- Режим: каждая сессия отдельным запуском, без истории
- Скорость: три прогретых повтора на конфигурации API замеров (см. выше), медиана записана; TTFT не измеряется

Подготовка профилей OpenCode:
- Добавлен агент B в demo/opencode.json: agent.local-guide-b с prompt repo-system-b.txt
- Файл practices/practice_03/lab/demo/repo-system-b.txt создан

A/B ответы и события инструментов:
- Для каждого вопроса получены фактические вызовы инструментов (read, при необходимости glob/grep). В ответах указывались пути и строки.
- Наблюдение: обе конфигурации A и B корректно не выдумывают CI и функции, различаются стилем: B сначала цитирует строки, затем вывод; A сразу даёт краткий ответ с file:line.

Файлы результатов A/B (jsonl):
- practices/practice_03/lab/results/hw_A_q1.jsonl … hw_A_q5.jsonl
- practices/practice_03/lab/results/hw_B_q1.jsonl … hw_B_q5.jsonl

Замеры скорости (медианы прогретых повторов, по JSON-логам API экспериментов system):
- hot42/hot43/hot44 (temperature 0.8) median wall_seconds ≈ 6.48s / 8.03s / 9.27s; median decode_tps ≈ 84.9 / 86.3 / 89.2
- cold42/cold43/cold44 (temperature 0.2) median wall_seconds ≈ 10.71s / 11.39s / 12.94s; median decode_tps ≈ 80.6 / 73.0 / 75.9

Ошибки/границы возможностей:
- Вопрос о CI: в материалах нет конфигурации CI — обе версии агента отвечают об отсутствии сведений и ссылаются на README.md:6.
- unsubscribe отсутствует в коде — агент B явно показывает отсутствие по результатам glob/read.

Вывод по A/B:
- Оставляем Prompt B (repo-system-b.txt): он дисциплинирует формат ответа (цитаты file:line перед выводом) и снижает риск импровизаций при тех же правах и модели.
