# Word Statistics API

##  Описание проекта

API для анализа частотности словоформ слова "житель" в текстовых файлах. Проект разработан с использованием **FastAPI** и архитектурным подходом **DDD (Domain-Driven Design)**.

### Функциональность:
- Загрузка текстовых файлов (.txt, .doc, .docx)
- Анализ всех словоформ слова "житель" (житель, жителя, жителю, жителем, жители и т.д.)
- Подсчет статистики:
  - Общее количество каждой словоформы
  - Количество в каждой строке текста
- Экспорт результатов в Excel (.xlsx)
- Асинхронная обработка больших файлов
- Многопользовательский режим с ограничением concurrent задач

##  Архитектура (DDD)
word-statistics/
├── backend/ # FastAPI бэкенд
│ ├── app/
│ │ ├── domain/ # Доменный слой
│ │ │ ├── entities/ # Сущности
│ │ │ ├── value_objects/ # Объекты-значения
│ │ │ └── interfaces/ # Интерфейсы репозиториев
│ │ ├── application/ # Слой приложения
│ │ │ ├── services/ # Сервисы
│ │ │ └── dtos/ # Data Transfer Objects
│ │ ├── infrastructure/ # Инфраструктура
│ │ │ ├── repositories/ # Репозитории (Excel)
│ │ │ ├── parsers/ # Парсеры файлов
│ │ │ └── workers/ # Фоновые задачи
│ │ └── api/ # API слой
│ │ └── routes/ # Эндпоинты
│ ├── results/ # Папка с результатами
│ ├── uploads/ # Папка для загрузок
│ ├── main.py
│ └── requirements.txt
├── frontend/ # React + Vite фронтенд
│ ├── src/
│ │ ├── components/
│ │ │ └── FileUploader.tsx
│ │ ├── App.tsx
│ │ └── main.tsx
│ └── package.json
├── docker-compose.yml
└── README.md

##  Установка и запуск

### Вариант 1: Локальный запуск

#### Требования:
- Python 3.12+
- Node.js 18+
- Git

#### Бэкенд:
```bash
# Клонирование репозитория
git clone <url-репозитория>
cd word-statistics/backend

# Создание виртуального окружения
python -m venv venv

# Активация (Windows)
venv\Scripts\activate
# Или (Linux/Mac)
# source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Запуск
uvicorn main:app --reload --host 0.0.0.0 --port 8000
Фронтенд
# Новый терминал
cd word-statistics/frontend

# Установка зависимостей
npm install

# Запуск
npm run dev
Вариант 2: Запуск через Docker
Требования:
Docker Desktop

Docker Compose

bash
# Клонирование репозитория
git clone <url-репозитория>
cd word-statistics

# Запуск всех сервисов
docker-compose up -d

# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down
Вариант 3: Скрипт для Windows
powershell
# Запустить start.ps1 (откроет два окна: бэкенд и фронтенд)
.\start.ps1
 API Эндпоинты
POST /api/v1/analysis/upload
Загрузка файла для анализа

Параметры:

file: текстовый файл (.txt, .doc, .docx)

Ответ:

json
{
  "task_id": "uuid",
  "status": "queued",
  "message": "Файл принят в обработку"
}
GET /api/v1/analysis/status/{task_id}
Получение статуса обработки

Ответ:

json
{
  "status": "processing",
  "progress": 50,
  "message": "Анализ текста"
}
GET /api/v1/analysis/download/{task_id}
Скачивание результата (Excel файл)

Тестирование
Пример тестового файла test.txt:
text
В городе жил один житель.
Этот житель часто ходил к другому жителю.
Жители города собрались вместе.
Разговор с жителем был интересным.
Ожидаемый результат в Excel:
Словоформа	Кол-во во всём документе	Кол-во в каждой строке
житель	2	1,1,0,0
жителю	1	0,1,0,0
жители	1	0,0,1,0
жителем	1	0,0,0,1
 Особенности реализации
Асинхронная обработка
Файлы обрабатываются в фоновых задачах

Не блокирует API для других пользователей

Поддержка файлов до 100MB

Ограничение concurrent задач
Максимум 5 параллельных задач

Очередь для остальных запросов

Масштабирование
Docker-контейнеры для легкого масштабирования

Возможность добавления нескольких экземпляров бэкенда

Redis для распределенных задач (в разработке)

Технологии
Бэкенд:
Python 3.12

FastAPI

Pandas / OpenPyXL (Excel)

Uvicorn

Pydantic

Фронтенд:
React 18

TypeScript

Vite

Ant Design

Axios

React Dropzone

DevOps:
Docker

Docker Compose

Nginx

Структура API
text
http://localhost:8000/          # Главная
http://localhost:8000/docs      # Swagger документация
http://localhost:8000/redoc     # ReDoc документация
http://localhost:8000/health    # Проверка здоровья
Безопасность
Ограничение размера файлов (100MB)

Валидация типов файлов

Санитизация входных данных

Изоляция задач

Деплой
На сервер с Docker:
bash
# Копирование файлов на сервер
scp -r word-statistics user@server:/app/

# Запуск
cd /app/word-statistics
docker-compose up -d
Настройка домена:
nginx
# Nginx конфигурация
server {
    listen 80;
    server_name ваш-домен.ru;

    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
    }

    location /api/ {
        proxy_pass http://localhost:8000/api/;
        proxy_set_header Host $host;
    }
}
Автор
Семененко Л.М.



 Выполненные требования
FastAPI реализация

Обработка текстовых файлов

Анализ словоформ "житель"

Статистика по строкам

Excel экспорт

Асинхронная обработка больших файлов

Многопользовательский режим

DDD архитектура

Docker контейнеризация

Фронтенд для тестирования

text

## Сохраните файл и отправьте:
1. Архив с проектом
2. Ссылку на GitHub
3. Резюме

**Всё готово к отправке!** 
