# Recommandations Service

Service that'll permit to have recommandations based on other's user notes.

# Setup

## Git Submodules

First of all, if you just cloned the repo, initialize the git submodules : 

```bash
make init-submodules
```

Then update them :
```bash
make update-submodules
```

## Dependancies

In order to intsall NLP's and grpc's python dependancies, use the requirements.txt:

```bash
pip install -r requirements.txt
```

### Download language models (spacy)

Add the name of the `spacy`'s model to download in the `models_array` and run the script

```bash
models_array=("fr_dep_news_trf")
```

```bash
misc/download_languages.sh
```
## Generate protobuf files

Run the bash script in the `misc` folder

```bash
misc/gen_proto.sh
```

# Run the service

```bash
python3 recommendations-service.py
```

# Docker

In order to build the `recommendations-service` docker image use the Makefile rule:

```bash
make build 
```

Same for running

```bash
make run
```

By default the service runs on the 3000 port.