# Docker Flask App — Учебный проект по Docker

Полный проект по 10 заданиям по Docker: от базовых команд до CI/CD с GitHub Actions.

## Структура проекта

```
docker-project/
├── app.py                      # Flask-приложение (Задания 2-8)
├── requirements.txt            # Зависимости Python
├── Dockerfile                  # Задание 2, 6, 8
├── docker-compose.yml          # Задание 3, 4, 5, 7
├── docker-stack.yml            # Задание 9 (Docker Swarm)
├── .env                        # Задание 7 (переменные окружения)
├── .dockerignore               # Задание 8 (безопасность)
├── .github/workflows/
│   └── docker-build.yml        # Задание 10 (CI/CD)
└── screenshots/                 # PNG для отчёта
```

## Быстрый старт

```bash
# 1. Сборка и запуск всех сервисов
docker compose up --build -d

# 2. Проверка
curl http://localhost:5000
curl http://localhost:5000/health
curl http://localhost:5000/info

# 3. pgAdmin доступен на http://localhost:5050
# Логин: admin@example.com / пароль: admin

# 4. Остановка
docker compose down

# 5. Остановка с удалением volumes (данные будут потеряны)
docker compose down -v
```

## Задания

| # | Тема | Файлы |
|---|------|-------|
| 1 | Базовые команды Docker | `docker run hello-world`, `docker run -it ubuntu bash` |
| 2 | Dockerfile для Flask | `Dockerfile`, `app.py` |
| 3 | Docker Compose (3 сервиса) | `docker-compose.yml` |
| 4 | Volumes | `docker-compose.yml` (volumes section) |
| 5 | Сети и изоляция | `docker-compose.yml` (networks section) |
| 6 | Multi-stage build | `Dockerfile` (builder + runtime) |
| 7 | Переменные окружения | `.env`, `docker-compose.yml` |
| 8 | Безопасность | `Dockerfile` (USER), `.dockerignore` |
| 9 | Docker Swarm | `docker-stack.yml` |
| 10 | CI/CD GitHub Actions | `.github/workflows/docker-build.yml` |

## API Endpoints

- `GET /` — Hello, Docker!
- `GET /health` — Проверка здоровья приложения и БД
- `GET /info` — Информация о контейнере и переменных окружения
- `GET /api/messages` — Получить сообщения из БД
- `POST /api/messages` — Добавить сообщение в БД

## Требования

- Docker Desktop 24+
- Docker Compose v2
