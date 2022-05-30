# Script used to download wanted languages models used by python package `spacy` (used by`pke`, the current keyword extraction toolkit)  
#!/bin/bash

models_array=("fr_dep_news_trf")

for model in ${models_array[*]}; do
    python -m spacy download $model
done
