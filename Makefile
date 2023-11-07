build:
	docker-compose build
start: # Запуск контейнеров сервиса
	docker-compose up

stop: # Остановка контейнеров сервиса
	docker-compose down

#create-book: # Команда для создания книги
#	poetry run python backend/...