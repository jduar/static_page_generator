.PHONY: lint run generate thumbnails

run: public
	docker compose up --build -d

generate: public
	docker compose run --rm generator python src/main.py

thumbnails: public
	docker compose run --rm generator python src/main.py --generate-thumbnails $(if $(FORCE),--force,)

public:
	mkdir -p public

lint:
	uv run ruff check src
