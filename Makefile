# Run the protoc compiler to generate the Golang server code.
codegen: update-submodules
	docker run --rm -v `pwd`/grpc:/app/grpc -v `pwd`/misc:/app/misc -w /app noted-py-protoc /bin/sh -c misc/gen_proto.sh 

# Fetch the latest version of the protos submodule.
update-submodules:
	git submodule update --remote

# After cloning the repo, run init
init:
	git submodule init
	docker build -t noted-py-protoc -f misc/Dockerfile .
