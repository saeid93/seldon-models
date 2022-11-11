ISTIO_PORT ?= 8003

deploy:
	kubectl apply -f manifest.yaml

remove:
	kubectl delete -f manifest.yaml

meta:
	curl -s http://localhost:${ISTIO_PORT}/seldon/seldon/v2-sklearn-iris/v2/models/classifier | jq .

rest:
	curl -v -s -H 'Content-Type: application/json' \
		-d @request-rest.json \
		http://localhost:${ISTIO_PORT}/seldon/seldon/v2-sklearn-iris/v2/models/infer | jq .

grpc:
	cat request-grpc.json | grpcurl -d '@' -plaintext -proto ./proto/dataplane.proto \
		-rpc-header seldon:v2-sklearn-iris -rpc-header namespace:seldon \
		localhost:${ISTIO_PORT} inference.GRPCInferenceService/ModelInfer
