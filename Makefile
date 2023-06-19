IMAGE = ondrejsika/demo-cloud-provider
CONTAINER = demo-cloud-provider

all: build push

build:
	docker build --platform linux/amd64 -t $(IMAGE) .

push:
	docker push $(IMAGE)

run:
	docker run -d --name $(CONTAINER) -p 8000:8000 $(IMAGE)

stop:
	docker rm -f $(CONTAINER)
