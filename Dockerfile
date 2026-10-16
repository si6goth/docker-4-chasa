# ============================================================
# Задание 2: Базовый Dockerfile для Flask-приложения
# Задание 6: Multi-stage build (два этапа)
# Задание 8: Безопасность (non-root пользователь)
# ============================================================

# --- Этап 1: Build (сборка зависимостей) ---
FROM python:3.11-slim AS builder

WORKDIR /app

# Копируем только requirements для кэширования layers
COPY requirements.txt .

# Устанавливаем зависимости в виртуальное окружение
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# --- Этап 2: Runtime (финальный образ) ---
FROM python:3.11-slim

# Метка образа
LABEL maintainer="docker-student"
LABEL description="Flask application with PostgreSQL"

# Переменные окружения (не выводить buffer в stdout)
ENV PYTHONUNBUFFERED=1

# Рабочая директория
WORKDIR /app

# Копируем виртуальное окружение из builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Копируем исходный код
COPY app.py .

# (Задание 8) Создаём non-root пользователя для безопасности
RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /sbin/nologon appuser \
    && chown -R appuser:appuser /app \
    && mkdir -p /app/logs \
    && chown -R appuser:appuser /app/logs

# Переключаемся на non-root пользователя
USER appuser

# Открываем порт
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# Команда запуска
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--access-logfile", "-", "app:app"]
