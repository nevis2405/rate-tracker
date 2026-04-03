up:
	docker-compose up --build

down:
	docker-compose down

seed:
	docker-compose exec web python manage.py seed_data

test:
	docker-compose exec web pytest

logs:
	docker-compose logs -f