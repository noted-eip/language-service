FROM python:3.10-alpine

# TODO : Change to python venv or keep the "docker-user" - Pbbly not as simple as it seems

WORKDIR /app

# Install protobuf
RUN apk update && apk add --no-cache make protobuf-dev=3.18.1-r1

# Create user to not use pip as root and give according ownership to manipulate future files
RUN adduser -D docker-user
RUN chown docker-user:docker-user .
USER docker-user
ENV PATH="/home/docker-user/.local/bin:${PATH}"

# Upgrade pip (last flag supress current version warning)
RUN python3 -m pip install --upgrade pip --disable-pip-version-check

# Copy every file and give the right permissions/ownership
COPY --chown=docker-user:docker-user . .

# Install proto-dependencies
RUN pip install -r requirements.txt

RUN ./misc/gen_proto.sh
RUN ./misc/download_language_models.sh

ENTRYPOINT [ "python3", "recommendations-service.py" ]

