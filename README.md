# EFO - embeddings

**Embeddings for the EFO_OT_slim are in the asset release of this repo**

Following steps can be used to calculate embeddings on other ontologies/reproduce obtained results.

## Reproduce the environment 

(Steps for Linux, if running in Windows: use WSL)

1. Clone the repository 


2. The required python version is 3.8, the easiest way is to create a conda environment with:

```
conda create -n owl2vec python=3.8 "setuptools<65"
conda activate owl2vec
```

3. Install `uv` and run `uv sync` in the repository folder. 

4. Make sure to `cd` in the repo folder and run:
```
sh scripts/1_get_data.sh
uv run python scripts/2_get_punkt.py
uv run python scripts/3_extract_entities.py
```

## Calculate and extract embeddings (in output folder)
Simply run:

```
sh scripts/4_train.sh
uv run python scripts/5_extract_embeddings.py
```

Embeddings are in the `embeddings` folder.

