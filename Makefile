.PHONY: lint run generate thumbnails

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
