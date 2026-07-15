# %%
import gensim
from owlready2 import *
import polars as pl
import numpy as np
import zipfile
from rich import print
from rich.console import Console

console = Console()

console.print("Loading ontology and model", style="bold red")

word2vec_embedding_file = "./embeddings/ontology.embeddings"
onto_file = "./data/efo_otar_slim.owl"

model = gensim.models.Word2Vec.load(word2vec_embedding_file)
onto = get_ontology(onto_file).load()
classes = list(onto.classes())


all_classes_iri = [c.iri for c in classes]

print(f"Number of class iri: {len(all_classes_iri)}")

console.print("Loading diseases", style="bold red")
disease_df = pl.read_parquet("./data/disease/disease.parquet")


disease_iri_codes = disease_df['code'].to_list()

# are all OT disease codes in EFO_slim iri? --> YES

print(f"N. of OT diseases: {len(set(disease_iri_codes))}")
print(f"N. of intersection: {len(set(disease_iri_codes) & set(all_classes_iri))}")


def get_embedding(iri):
    return model.wv.get_vector(iri).astype(np.float32).tolist()

console.print("Extract embeddings", style="bold red")
embeddings = pl.DataFrame({'iri': disease_iri_codes}).with_columns(
    pl.col("iri")
    .map_elements(
        get_embedding,
        return_dtype=pl.List(pl.Float32)
    )
    .alias("embeddings")
)


console.print("Dump embeddings", style="bold red")
embeddings.write_parquet("./output/efo_owl_embeddings.parquet", compression="brotli")

with zipfile.ZipFile("./output/efo_owl_embeddings.zip", 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.write("./output/efo_owl_embeddings.parquet", arcname="efo_owl_embeddings.parquet")

console.print("Success!", style="bold green")