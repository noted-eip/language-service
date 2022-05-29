# Recommandations Service

Service that'll permit to have recommandations based on other's user notes.

# Quick setup

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

## Run the service

```bash
python3 recommendations-service.py
```