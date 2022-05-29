# This image is meant for building the recommendations-service and generating
# protobuf code in a consistent way.
FROM python:3.10-slim as build

RUN apt update && apt install g++ make git -y

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install --upgrade pip

COPY . .

RUN pip install -r requirements.txt

RUN ./misc/gen_proto.sh
RUN ./misc/download_language_models.sh


# Not sure if multistaged is useful here, keep it like that if it is
FROM python:3.10-slim

COPY --from=build grpc ./recommendations-service.py .env ./
COPY --from=build /opt/venv /opt/venv

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN python3 -m venv $VIRTUAL_ENV

ENTRYPOINT [ "python3", "recommendations-service.py" ]

EXPOSE 3000
