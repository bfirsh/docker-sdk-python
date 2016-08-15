.PHONY: all build test

ARGS := tests

all: test

build:
	docker build -t docker-sdk-python .

test: build
	docker run --rm -v /var/run/docker.sock:/var/run/docker.sock docker-sdk-python py.test $(ARGS)

shell: build
	docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock docker-sdk-python python
