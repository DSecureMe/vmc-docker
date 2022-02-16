v ?= 1.2rc3

all: build

build:
	docker build -f Dockerfile.vmc-builder --build-arg VMC_VERSION=$(v) -t vmc-builder .
	docker build -f Dockerfile.nginx --build-arg VMC_VERSION=$(v) -t vmc-static-nginx .
	docker build -f Dockerfile.vmc --build-arg VMC_VERSION=$(v) -t vmc .

.PHONY: build

