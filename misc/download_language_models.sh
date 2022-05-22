models_array=("fr_dep_news_trf")

for model in ${models_array[*]}; do
    python -m spacy download $model
done
