# Загружает зависимости проекта
install:
	uv sync


# Проверяет код в папке page_analyzer на соответствие правилам линтера из ruff.toml
lint:
	uv run ruff check page_analyzer


# Исправляет замечания линтера, не связанные с логикой (порядок импортов, пробелы, и т.д.)
fix:
	uv run ruff check --fix page_analyzer


# Прогоняет все тесты
test:
	uv run pytest

# Проверяет покрытие кода тестами и формирует отчет в файле coverage.xml
# Далее этот файл использует SonarCloud для анализа
test-coverage:
	uv run pytest --cov=page_analyzer --cov-report xml

# Прогоняет сначала тесты, потом проверку линтером
check: test lint


# Запускает скрипт для установки uv и зависимостей проекта для платформы render.com
build:
	./build.sh


# Запускает локальный сервер
dev:
	uv run flask --debug --app page_analyzer:app run


# Запускает приложение в режиме продакшена. 
# Приложение будет доступно по адресу http://localhost:8000, 
# если в переменных окружения не указан порт, необходимый для деплоя
PORT ?= 8000
start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app


# Запускает сервер в продакшене на платформе render.com (там все зависимости устанавливаются глобально)
render-start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app


# Команды, которые могут совпадать с именами директорий и не должны быть с ними перепутаны
.PHONY: install test lint selfcheck check build