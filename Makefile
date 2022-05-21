# Run the protoc compiler to generate the Golang server code.
codegen: update-submodules
	echo `pwd`
	docker run --rm -v `pwd`/grpc:/app/grpc -v `pwd`/misc:/app/misc -w /app noted-python-protoc /bin/sh -c misc/gen_proto.sh

# Fetch the latest version of the protos submodule.
update-submodules:
	git submodule update --remote

# After cloning the repo, run init
init:
	git submodule init
	docker build -t noted-python-protoc -f misc/Dockerfile .
