# Init submodules
init-submodules:
	git submodule init

# Fetch the latest version of the protos submodule.
update-submodules:
	git submodule update --remote

build: init-submodules update-submodules
	docker build -t language-service -f Dockerfile .

run:
	docker run -p 3000:3000 language-service
