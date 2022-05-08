rm -rf grpc/*pb/
protoc --go_out=. --go-grpc_out=. grpc/protos/recommendations/*.proto --proto_path=./grpc/protos