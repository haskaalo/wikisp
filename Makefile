.PHONY: build-image
build-image:
	cd shortestpath && docker build -t webapp-server:latest -f ./webapp/Dockerfile --build-arg RECAPTCHA_SITEKEY .

.PHONY: run-webapp
run-webapp:
	cd shortestpath/webapp && docker-compose up -d

.PHONY: stop-webapp
stop-webapp:
	cd shortestpath/webapp && docker-compose down