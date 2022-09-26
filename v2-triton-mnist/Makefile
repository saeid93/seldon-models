LOG_VERBOSE ?= 0

ISTIO_PORT ?= 8003
HTTP_SERVICE_PORT ?= 8000

BATCH_WORKERS ?= 10
BATCH_BINARY_PAYLOADS ?= true
BATCH_INPUT_FILE ?= "batch-input.txt"
BATCH_OUTPUT_FILE ?= "batch-output.txt"


############################ LOCAL TESTING ###############################

install:
	poetry install

train:
	poetry run python3 train.py

prepare-batch:
	python3 prepare-batch-input.py

serve:
	docker run --rm -p ${HTTP_SERVICE_PORT}:8000 -p 8001:8001 -p 8002:8002 \
	-v ${PWD}/models-repository:/models nvcr.io/nvidia/tritonserver:21.08-py3 tritonserver --model-repository=/models  --log-verbose ${LOG_VERBOSE}

local-live:
	curl -v http://localhost:${HTTP_SERVICE_PORT}/v2/health/live

local-ready:
	curl -v http://localhost:${HTTP_SERVICE_PORT}/v2/health/ready

local-meta:
	curl -s http://localhost:${HTTP_SERVICE_PORT}/v2/models/mnist | jq .

local-config:
	curl -s http://localhost:${HTTP_SERVICE_PORT}/v2/models/mnist/config | jq .

local-rest:
	curl -v -s -H 'Content-Type: application/json' \
		-d @request.json \
		http://localhost:${HTTP_SERVICE_PORT}/v2/models/mnist/infer | jq .

local-batch:
	mlserver infer -u localhost:${HTTP_SERVICE_PORT} -m mnist -i ${BATCH_INPUT_FILE} -o ${BATCH_OUTPUT_FILE} -b ${BATCH_BINARY_PAYLOADS} --workers ${BATCH_WORKERS}


############################## K8s TESTING #################################

minio:
	rclone copy models-repository minio:triton-models/mnist-model

deploy:
	kubectl apply -f manifest.yaml

remove:
	kubectl delete -f manifest.yaml

meta:
	curl -s http://localhost:${ISTIO_PORT}/seldon/seldon/v2-triton-mnist/v2/models/mnist | jq .

rest:
	curl -v -s -H 'Content-Type: application/json' \
		-d @request.json \
		http://localhost:${ISTIO_PORT}/seldon/seldon/v2-triton-mnist/v2/models/mnist/infer | jq .

batch:
	mlserver infer -u localhost:${ISTIO_PORT}/seldon/seldon/v2-triton-mnist -m mnist -i ${BATCH_INPUT_FILE} -o ${BATCH_OUTPUT_FILE} -b ${BATCH_BINARY_PAYLOADS} --workers ${BATCH_WORKERS}
