MLSERVER_DIR ?= ${HOME}/work/MLServer

ISTIO_PORT ?= 8003
HTTP_SERVICE_PORT ?= 8080
GRPC_SERVICE_PORT ?= 8081

BATCH_WORKERS ?= 10
BATCH_INPUT_FILE ?= "batch-input.txt"
BATCH_OUTPUT_FILE ?= "batch-output.txt"


############################ LOCAL TESTING ###############################

install:
	poetry install

train:
	poetry run python3 train.py

serve:
	poetry run mlserver start .

prepare-batch:
	python3 prepare-batch-input.py

local-live:
	curl -v http://localhost:${HTTP_SERVICE_PORT}/v2/health/live

local-ready:
	curl -v http://localhost:${HTTP_SERVICE_PORT}/v2/health/ready

local-meta:
	curl -s http://localhost:${HTTP_SERVICE_PORT}/v2/models/mnist-svm | jq .

local-rest:
	curl -v -s -H 'Content-Type: application/json' \
		-d @request-rest.json \
		http://localhost:${HTTP_SERVICE_PORT}/v2/models/mnist-svm/versions/v0.1.0/infer | jq .

local-grpc:
	cat request-grpc.json | grpcurl -d '@' -plaintext -proto ./proto/dataplane.proto \
		localhost:8081 inference.GRPCInferenceService/ModelInfer

local-batch:
	mlserver infer -u localhost:${HTTP_SERVICE_PORT} -m mnist-svm -i ${BATCH_INPUT_FILE} -o ${BATCH_OUTPUT_FILE} --workers ${BATCH_WORKERS} -v


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
		-d @request-rest.json \
		http://localhost:${ISTIO_PORT}/seldon/seldon/v2-sklearn-mnist/v2/models/infer | jq .

grpc:
	cat request-grpc.json | grpcurl -d '@' -plaintext -proto ./proto/dataplane.proto \
		-rpc-header seldon:v2-sklearn-mnist -rpc-header namespace:seldon \
		localhost:${ISTIO_PORT} inference.GRPCInferenceService/ModelInfer

batch:
	mlserver infer -u localhost:${ISTIO_PORT}/seldon/seldon/v2-sklearn-mnist -m mnist-svm -i ${BATCH_INPUT_FILE} -o ${BATCH_OUTPUT_FILE} --workers ${BATCH_WORKERS} -v
