# Пошаговый план разработки

## 1. Подготовка среды
Установите Git, Docker Desktop с Compose, Node.js 24 LTS, Python 3.11+ и uv. Убедитесь, что запускаются `git --version`, `docker compose version`, `node -v`, `python --version` и `uv --version`.

## 2. Создание репозитория
Создайте GitHub-репозиторий, включите README, лицензию и `.gitignore`. Настройки окружения храните в `.env`, не коммитьте пароли или другие секреты.

## 3. Backend и схема данных
Определите поля входного запроса и результата. Реализуйте FastAPI с Pydantic-валидацией, SQLAlchemy-моделью прогноза, сервисом, REST-маршрутами и `/health`. Документация OpenAPI доступна в `/docs`.

## 4. ML-пайплайн
Прототип использует WDBC через `sklearn.datasets.load_breast_cancer`, положительный класс malignant,
стратифицированный split 80/20 с seed 42 и pipeline StandardScaler + LogisticRegression. Holdout-метрики
accuracy/precision/recall/ROC-AUC доступны через API. WDBC не содержит исходов лечения, поэтому вероятность
malignant нельзя трактовать как прогноз эффективности терапии или клинический показатель.

## 5. Миграции и тесты
Настройте Alembic, создайте начальную миграцию и автоматические тесты API/модели. Выполните `uv sync`, `uv run alembic upgrade head`, `uv run pytest -q` и `uv run ruff check .` в backend.

## 6. Frontend
Создайте русскоязычные страницы ввода, результата и истории. Обозначьте ограничения модели и запрет на применение к реальным пациентам. Проверьте ESLint, TypeScript и production build.

## 7. Docker Compose и CI
Соберите Next.js, FastAPI и PostgreSQL, добавьте readiness healthcheck и автоматический запуск миграций. Настройте GitHub Actions для тестов backend, lint/typecheck/build frontend.

## 8. Документация и выпуск
Опишите архитектуру, команды запуска, API, датасет и ограничения в README/architecture. Перед любым применением в медицине потребуются независимая клиническая валидация, анализ справедливости и регуляторная экспертиза; данный прототип не предназначен для такого применения.
