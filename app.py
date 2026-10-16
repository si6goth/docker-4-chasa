"""
Flask-приложение для Docker-проекта.
Задания 2-8: базовое веб-приложение с подключением к PostgreSQL.
"""
import os
import sys
from flask import Flask, jsonify, request

app = Flask(__name__)

# Конфигурация из переменных окружения (Задание 7)
APP_ENV = os.getenv('APP_ENV', 'development')
SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:pass@db:5432/mydb')


def get_db_config():
    """Парсит DATABASE_URL и возвращает конфиг для psycopg2."""
    # Формат: postgresql://user:pass@host:port/dbname
    from urllib.parse import urlparse
    parsed = urlparse(DATABASE_URL)
    return {
        'host': parsed.hostname or 'db',
        'port': parsed.port or 5432,
        'dbname': parsed.path.lstrip('/') or 'mydb',
        'user': parsed.username or 'user',
        'password': parsed.password or 'pass'
    }


def init_db():
    """Инициализирует таблицу в базе данных."""
    try:
        import psycopg2
        config = get_db_config()
        conn = psycopg2.connect(**config)
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                text VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        cur.close()
        conn.close()
        print(f"[{APP_ENV}] Database initialized successfully")
    except ImportError:
        print("psycopg2 not installed, skipping DB initialization")
    except Exception as e:
        print(f"DB init warning: {e}")


@app.route('/')
def index():
    """Главная страница - возвращает Hello, Docker! (Задание 2)"""
    return jsonify({
        'message': 'Hello, Docker!',
        'environment': APP_ENV,
        'status': 'running'
    })


@app.route('/health')
def health():
    """Проверка здоровья приложения и подключения к БД."""
    db_status = 'unknown'
    try:
        import psycopg2
        config = get_db_config()
        conn = psycopg2.connect(**config)
        conn.close()
        db_status = 'connected'
    except ImportError:
        db_status = 'psycopg2 not installed'
    except Exception as e:
        db_status = f'error: {str(e)}'

    return jsonify({
        'app_status': 'healthy',
        'environment': APP_ENV,
        'database': db_status
    })


@app.route('/api/messages', methods=['GET'])
def get_messages():
    """Получить все сообщения из БД."""
    try:
        import psycopg2
        config = get_db_config()
        conn = psycopg2.connect(**config)
        cur = conn.cursor()
        cur.execute('SELECT id, text, created_at FROM messages ORDER BY created_at DESC')
        rows = cur.fetchall()
        messages = [{'id': r[0], 'text': r[1], 'created_at': str(r[2])} for r in rows]
        cur.close()
        conn.close()
        return jsonify({'messages': messages})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/messages', methods=['POST'])
def add_message():
    """Добавить сообщение в БД (Задание 3 - проверка записи)."""
    data = request.get_json() or {}
    text = data.get('text', '')
    if not text:
        return jsonify({'error': 'text is required'}), 400
    try:
        import psycopg2
        config = get_db_config()
        conn = psycopg2.connect(**config)
        cur = conn.cursor()
        cur.execute('INSERT INTO messages (text) VALUES (%s) RETURNING id, text, created_at', (text,))
        row = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({
            'message': 'Message saved',
            'id': row[0],
            'text': row[1],
            'created_at': str(row[2])
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/info')
def info():
    """Информация о контейнере (Задание 7 - проверка переменных окружения)."""
    return jsonify({
        'environment': APP_ENV,
        'hostname': os.getenv('HOSTNAME', 'unknown'),
        'secret_key_set': bool(SECRET_KEY and SECRET_KEY != 'default-secret-key'),
        'database_url_configured': bool(DATABASE_URL),
        'python_version': sys.version,
        'docker_container': 'yes'
    })


if __name__ == '__main__':
    print(f"Starting Flask app in {APP_ENV} mode...")
    init_db()
    debug_mode = APP_ENV != 'production'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
