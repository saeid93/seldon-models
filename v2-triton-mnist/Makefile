ISTIO_PORT ?= 8003

############################ LOCAL TESTING ###############################

install:
	poetry install

train:
	poetry run python3 train.py

serve:
	docker run --rm -p 8000:8000 -p 8001:8001 -p 8002:8002 \
	-v ${PWD}/models-repository:/models nvcr.io/nvidia/tritonserver:21.08-py3 tritonserver --model-repository=/models

local-meta:
	curl -s http://localhost:8000/v2/models/mnist | jq .

local-rest:
	curl -v -s -H 'Content-Type: application/json' \
		-d @request.json \
		http://localhost:8000/v2/models/mnist/infer | jq .


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
