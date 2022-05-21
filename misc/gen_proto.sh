rm -rf grpc/*pb/
python -m grpc_tools.protoc --python_out=./grpc --grpc_python_out=./grpc grpc/protos/recommendations/*.proto --proto_path=./grpc/protos
