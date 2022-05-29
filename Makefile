# Init submodules
init-submodules:
	git submodule init

# Fetch the latest version of the protos submodule.
update-submodules:
	git submodule update --remote

build: init-submodules update-submodules
	docker build -t recommendations-service -f Dockerfile .

run:
	docker run recommendations-service -d -p 8080:8080
