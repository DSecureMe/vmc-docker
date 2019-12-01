v ?= 1.0.1-alpha

all: build

build:
	docker build --build-arg VMC_VERSION=$(v) -t vmc .

.PHONY: build