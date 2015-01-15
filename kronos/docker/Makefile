SHELL := /bin/bash

ifndef KRONOS_VERSION
$(error Please specify a KRONOS_VERSION, like `KRONOS_VERSION=v0.7.0 make build`)
endif

generate_dockerfile:
	mkdir -p $(KRONOS_VERSION)
	sed -e "s/__TAG__/$(KRONOS_VERSION)/" Dockerfile.template > $(KRONOS_VERSION)/Dockerfile
	cp supervisord.conf $(KRONOS_VERSION)
build:
	cd $(KRONOS_VERSION) && sudo docker build -t chronology/kronos:$(KRONOS_VERSION) .
build_nocache:
	cd $(KRONOS_VERSION) && sudo docker build --no-cache -t chronology/kronos:$(KRONOS_VERSION) .
run:
	sudo docker run -d -p 8150:8150 -v /etc/kronos:/etc/kronos -v /var/log/kronos:/var/log/kronos chronology/kronos:$(KRONOS_VERSION)
run-terminal:
	sudo docker run -t -i chronology/kronos:$(KRONOS_VERSION) /bin/bash
push:
	sudo docker push chronology/kronos:$(KRONOS_VERSION)
ip:
	boot2docker ip
