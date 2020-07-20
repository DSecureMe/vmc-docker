v ?= 1.1-RC-1

all: build

build:
	docker run -i hadolint/hadolint < Dockerfile
	docker build --build-arg VMC_VERSION=$(v) -t vmc .

.PHONY: build