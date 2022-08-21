ISTIO_PORT ?= 8003
HTTP_SERVICE_PORT ?= 8080


############################ LOCAL TESTING ###############################

install:
	poetry install

train:
	poetry run python3 train.py

serve:
	poetry run mlserver start .

local-rest:
	curl -v -s -H 'Content-Type: application/json' \
		-d @request.json \
		http://localhost:${HTTP_SERVICE_PORT}/v2/models/mnist-svm/versions/v0.1.0/infer | jq .


############################## K8s TESTING #################################

minio:
	rclone copy settings.json minio:v2-sklearn-mnist
	rclone copy model-settings.json minio:v2-sklearn-mnist
	rclone copy mnist-svm.joblib minio:v2-sklearn-mnist

deploy:
	kubectl apply -f manifest.yaml

remove:
	kubectl delete -f manifest.yaml

meta:
	curl -s http://localhost:${ISTIO_PORT}/seldon/seldon/v2-sklearn-mnist/v2/models/mnist-svm | jq .

rest:
	curl -v -s -H 'Content-Type: application/json' \
		-d @request.json \
		http://localhost:${ISTIO_PORT}/seldon/seldon/v2-sklearn-mnist/v2/models/infer | jq .
