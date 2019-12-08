SHELL = /bin/bash
COMPOSE = compose

define compose-file
	-f $(COMPOSE)/docker-compose.$(1).yml
endef

VMC = $(call compose-file,postgresql) $(call compose-file,elastalert) $(call compose-file,hive) $(call compose-file,elk) $(call compose-file,vmc)

.PHONY: all

all:
	make build

build: build-elastalert
	@echo "Starting to build project"

build-elastalert:
	@echo "Starting to build elastalert"
	docker-compose $(call compose-file,elk) $(call compose-file,elastalert) build

up:
	docker-compose $(VMC) up

down:
	docker-compose $(VMC) down

clean-images:
	@echo "Deleting all containers"
	docker rm -f `docker ps -a -q` 2>/dev/null; true
	@echo "Deleting all images"
	docker rmi -f `docker images -q` 2>/dev/null; true

clean-volumes:
	@echo "Deleting all volumes"
	echo "y" | docker volume prune

clean: clean-images clean-volumes
	@echo "Deleting all networks"
	echo "y" | docker network prune
	@echo "Cleaning the rest"
	echo "y" | docker system prune