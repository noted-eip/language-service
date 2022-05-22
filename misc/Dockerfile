# This image is meant for building the recommendations-service and generating
# protobuf code in a consistent way.
FROM python:3.10-alpine

RUN apk update && apk add --no-cache make protobuf-dev=3.18.1-r1

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install --upgrade pip

# Install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt
