# This image is meant for building the recommendations-service and generating
# protobuf code in a consistent way.
FROM python:3.10-slim as build

WORKDIR /app

RUN apt update && apt install g++ make git -y

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install --upgrade pip

COPY . .

RUN --mount=type=cache,id=pip-cache,target=/root/.cache/pip pip install -r requirements.txt

RUN ./misc/download_language_models.sh

# Not sure if multistaged is useful here, keep it like that if it is
FROM python:3.10-slim

WORKDIR /app

COPY --from=build /app/*.py ./
COPY --from=build /app/utils ./utils
COPY --from=build /app/protorepo ./protorepo

COPY --from=build /opt/venv /opt/venv

ENV RECOMMENDATIONS_SERVICE_PORT=${PORT:-3000}

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN python3 -m venv $VIRTUAL_ENV

ENTRYPOINT [ "python3", "-u", "main.py" ]

EXPOSE 3000
