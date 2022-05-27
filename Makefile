# Init submodules
init-submodules:
	git submodule init

# Fetch the latest version of the protos submodule.
update-submodules:
	git submodule update --remote

# Builds a Docker image that'll run the recommendations service
service-build: init-submodules update-submodules
	docker build -t noted-recommendations-service -f Dockerfile .


# placeholder
service-run:
	docker run noted-recommendations-service -d -p 8080:8080
# placeholder




