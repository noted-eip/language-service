# This image is meant for building the recommendations-service and generating
# protobuf code in a consistent way.
FROM python:3.10-alpine

RUN apk update && apk add --no-cache make protobuf-dev=3.18.1-r1
RUN pip install --no-cache-dir grpcio-tools
RUN pip install --no-cache-dir googleapis-common-protos
