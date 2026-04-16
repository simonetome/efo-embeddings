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
```

## Calculate embeddings
Simply run:

```
uv run owl2vec_star standalone --config_file default.cfg
```

Embeddings are in the embeddings folder, the notebook in the `notebooks` folder shows how to manipulate them to compute similarities.

