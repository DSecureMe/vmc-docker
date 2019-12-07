v ?= 1.0.1-alpha

all: build

build:
	docker run -i hadolint/hadolint < Dockerfile
	docker build --build-arg VMC_VERSION=$(v) -t vmc .

.PHONY: build