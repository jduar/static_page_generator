.PHONY: dev lint run generate thumbnails

dev: public
	docker compose up -d
	uv run watchfiles "python src/main.py" templates static src data/pages

lint:
	uv run ruff check src

run: public
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d

generate: public
	docker compose -f docker-compose.yml -f docker-compose.prod.yml run --rm generator python src/main.py

thumbnails: public
	docker compose -f docker-compose.yml -f docker-compose.prod.yml run --rm generator python src/main.py --generate-thumbnails $(if $(FORCE),--force,)

public:
	mkdir -p public
