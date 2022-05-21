# This image is meant for building the accounts-service and generating
# protobuf code in a consistent way.
FROM python:3.10-alpine

RUN apk update && apk add --no-cache make protobuf-dev=3.18.1-r1
RUN pip install grpcio-tools
RUN pip install googleapis-common-protos
