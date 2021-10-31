CONTAINER_NAME=mywebsite

build:
	python3 generator.py
	docker build -t $(CONTAINER_NAME) .

run:
	docker run --rm -p 8080:80 $(CONTAINER_NAME)

run-daemon:
	docker run --rm --name $(CONTAINER_NAME) -d -p 8080:80 $(CONTAINER_NAME)

stop:
	docker stop $(CONTAINER_NAME)
