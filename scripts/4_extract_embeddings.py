# %%
import gensim
from owlready2 import *
import polars as pl
import numpy as np


word2vec_embedding_file = "./embeddings/ontology.embeddings"
onto_file = "./data/efo_otar_slim.owl"

model = gensim.models.Word2Vec.load(word2vec_embedding_file)
onto = get_ontology(onto_file).load()
classes = list(onto.classes())
c = classes[0]

iri_v = model.wv.get_vector(c.iri)

all_classes_iri = [c.iri for c in classes]

print(f"Number of class iri: {len(all_classes_iri)}")


disease_df = pl.read_parquet("./data/disease/disease.parquet")


disease_iri_codes = disease_df['code'].to_list()

# are all OT disease codes in EFO_slim iri? --> YES

print(f"N. of OT diseases: {len(set(disease_iri_codes))}")
print(f"N. of intersection: {len(set(disease_iri_codes) & set(all_classes_iri))}")


def get_embedding(iri):
    return model.wv.get_vector(iri).astype(np.float32).tolist()

embeddings = pl.DataFrame({'iri': disease_iri_codes}).with_columns(
    pl.col("iri")
    .map_elements(
        get_embedding,
        return_dtype=pl.List(pl.Float32)
    )
    .alias("embeddings")
)



embeddings.write_parquet("./output/embeddings.parquet", compression="brotli")



