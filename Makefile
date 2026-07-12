SERVICE := generator

.PHONY: dev first-run run generate thumbnails lint

dev: public
	docker compose up --build

first-run: public
	cp -n example_content/images/* data/images/
	cp -n example_content/pages/* data/pages/
	cp -n example_content/favicon.svg data/favicon.svg
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d

run: public
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d

generate: public
	docker compose run --rm $(SERVICE) python src/main.py

thumbnails:
	docker compose run --rm $(SERVICE) python src/main.py --generate-thumbnails $(if $(FORCE),--force,)

lint:
	docker compose run --rm $(SERVICE) ruff check src

public:
	mkdir -p public
