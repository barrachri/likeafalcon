# Some simple testing tasks (sorry, UNIX only).

SERVICE=service-likeafalcon
POSTGRES_PASSWORD=mysecretpassword
POSTGRES_USER=postgres
POSTGRES_DB=likeafalcon

lint:
	@tox -e isort,flake8

clean:
	@find . -name \*.pyc -delete

run-docker:
	@docker run -d --name streams -p 4222:4222 nats-streaming:0.6.0
	@docker run -d --name postgres -p 5432:5432 -e POSTGRES_DB=$(POSTGRES_DB) -e POSTGRES_USER=$(POSTGRES_USER) -e POSTGRES_PASSWORD=$(POSTGRES_PASSWORD) postgres:10.0

clean-docker:
	@docker rm -f streams
	@docker rm -f postgres

build:
	@docker build -t $(SERVICE) -f Dockerfile .

.PHONY: lint clean-docker build