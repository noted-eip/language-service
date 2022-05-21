rm -rf grpc/*pb/
python -m grpc_tools.protoc --python_out=. --grpc_python_out=. grpc/protos/recommendations/*.proto --proto_path=./grpc/protos
