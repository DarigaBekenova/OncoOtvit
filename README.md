# ОнкоОтвет — WDBC-демонстрация

Учебное веб-приложение для демонстрации машинного обучения на открытом наборе Breast Cancer Wisconsin
Diagnostic (WDBC). Прототип содержит Next.js-интерфейс, REST API на FastAPI, PostgreSQL с Alembic, Docker
Compose и ML-модель логистической регрессии из scikit-learn.

> **Важно:** это учебная классификация доброкачественного/злокачественного класса по признакам опухоли.
> Набор WDBC не содержит данных об эффективности лечения, поэтому приложение не прогнозирует ответ на
> терапию, не ставит диагноз и не даёт медицинских рекомендаций. Не используйте реальные пациентские данные.

Источник данных: `sklearn.datasets.load_breast_cancer` (WDBC, 569 записей, 30 числовых признаков).
Положительный класс модели — `malignant` (исходный таргет sklearn `0`). Разбиение стратифицированное
80/20 с `random_state=42`. Демонстрационные образцы берутся из тестовой части и имеют эталонную метку.

## Что умеет

- выбирать готовый WDBC-образец без ручного ввода 30 признаков;
- получать вероятность класса malignant и предсказанный класс benign/malignant;
- просматривать holdout-метрики accuracy/precision/recall/ROC-AUC;
- сохранять и просматривать историю классификаций;
- проверять API через Swagger UI на `/docs`.

## Запуск через Docker Compose

Требуются Docker Desktop с Compose. Из корня проекта:

```sh
docker compose up --build
```

- Web UI: http://localhost:3000
- API и документация: http://localhost:8000/docs
- Health check: http://localhost:8000/health

Остановка: `docker compose down`. Данные PostgreSQL сохраняются в named volume. Для полного удаления базы:
`docker compose down -v`.

Значения Compose по умолчанию предназначены только для локальной разработки. Перед публикацией замените
пароль базы и настройте production-конфигурацию.

## Локальный запуск без Docker

Нужны Python 3.11+, `uv`, Node.js 24+ и npm. Для backend используется SQLite по умолчанию; PostgreSQL можно
включить через `DATABASE_URL`.

Backend:

```sh
cd backend
uv sync
uv run alembic upgrade head
uv run uvicorn app.main:app --reload
```

Frontend в другом терминале:

```sh
cd frontend
npm install
API_URL=http://localhost:8000 npm run dev
```

PowerShell:

```powershell
$env:API_URL="http://localhost:8000"
npm run dev
```

## API

- `GET /health` — состояние процесса.
- `GET /api/v1/predictions/samples` — 4 фиксированных WDBC-образца с эталонным классом.
- `GET /api/v1/predictions/metrics` — holdout-метрики, размер выборки и доля train.
- `POST /api/v1/predictions?sample_name=...&reference_class=...` — классифицировать образец; тело:
  `{"features": {30 признаков WDBC}}`.
- `GET /api/v1/predictions?limit=20` — последние записи (1–100).

## Проверки

```sh
cd backend
uv run pytest -q
uv run ruff check .
```

```sh
cd frontend
npm run lint
npx tsc --noEmit
npm run build
```

GitHub Actions запускает lint и тесты backend, lint/typecheck/build frontend и сборку backend-образа.

## Пошаговый план разработки

1. Зафиксировать учебную задачу: классификация benign/malignant на WDBC, без утверждений об эффективности лечения.
2. Реализовать воспроизводимую загрузку WDBC, stratify split 80/20 и pipeline StandardScaler + LogisticRegression.
3. Перевести API, БД и валидацию на 30 признаков WDBC, образцы, метрики holdout и предупреждения.
4. Сделать выбор образца в один клик, отображение эталона, результата и истории.
5. Обновить README, архитектуру, план, миграцию и тесты.
6. Прогнать pytest/Ruff, ESLint/TypeScript/build и локальный end-to-end сценарий.
7. Для медицинского применения нужны отдельные клинические данные, валидация, анализ смещений и регуляторика;
   текущий прототип для этого непригоден.

## Структура

- `frontend/` — Next.js App Router и пользовательский интерфейс.
- `backend/app/modules/predictions/` — схемы, REST-маршруты, сервис, модель и ORM.
- `backend/alembic/` — миграции, актуальная цепочка заканчивается `0002_wdbc_predictions`.
- `docs/architecture.md` — архитектура, данные и API.
