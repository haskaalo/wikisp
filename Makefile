.PHONY: build-image
build-image:
	cd shortestpath && docker build -t webapp-server:latest -f ./webapp/Dockerfile --build-arg CAPTCHA_SITEKEY .

.PHONY: run-webapp
run-webapp:
	cd shortestpath/webapp && docker-compose up -d

.PHONY: stop-webapp
stop-webapp:
	cd shortestpath/webapp && docker-compose down

.PHONY: step1-dp
step1-dp:
	cd dump-processing && python3 main.py

.PHONY: step2-dp
step2-dp:
	cd dump-processing && python3 main.py --csvtodb

.PHONY: step3-dp
step3-dp:
	cd dump-processing && python3 main.py --partition

.PHONY: step4-dp
step4-dp:
	cd shortestpath/cmd && go run main.go

.PHONY: step5-dp
step5-dp:
	cd dump-processing && python3 main.py --cleanup

.PHONY: dump-processing
dump-processing: step1-dp step2-dp step3-dp step4-dp step5-dp