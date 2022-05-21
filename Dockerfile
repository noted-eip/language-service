FROM python:3.10-alpine

WORKDIR /app

# Install protobuf
RUN apk update && apk add --no-cache make protobuf-dev=3.18.1-r1

# Create user to not use pip as root
RUN adduser -D pip-user
USER pip-user
ENV PATH="/home/pip-user/.local/bin:${PATH}"

# Install/Upgrade pip
RUN python3 -m pip install --upgrade pip

# Copy every file and give the right permissions/ownership
COPY --chown=pip-user:pip-user . .

# Install proto-dependencies and generate code
RUN python3 -m pip install --no-cache-dir grpcio-tools
RUN python3 -m pip install --no-cache-dir googleapis-common-protos
RUN ./misc/gen_proto.sh

ENTRYPOINT [ "python3", "recommendations-service.py" ]

