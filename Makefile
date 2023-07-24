.PHONY: build-image
build-image:
	cd shortestpath && docker build -t webapp-server:latest -f ./webapp/Dockerfile .

.PHONY: run-webapp
run-webapp:
	cd shortestpath/webapp && docker-compose -d up

.PHONY: stop-webapp
stop-webapp:
	cd shortestpath/webapp && docker-compose down