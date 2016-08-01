.PHONY: all build test

all: test

build:
	docker build -t docker-sdk-python .

test: build
	docker run --rm -v /var/run/docker.sock:/var/run/docker.sock docker-sdk-python py.test tests

shell: build
	docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock docker-sdk-python python
