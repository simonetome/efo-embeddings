"""
Generate OWL2Vec*-compatible entities.txt from Open Targets disease.parquet.

Reads the 'code' column (containing entity URIs/IRIs, e.g. EFO terms),
deduplicates them, and writes one URI per line to the cache directory
so it can be used as `pre_entity_file` in owl2vec.cfg.

Usage:
    python generate_entities.py \
        --input ./data/disease.parquet \
        --output ./cache/entities.txt \
        --column code
"""

import argparse
import sys
from pathlib import Path

import pandas as pd


def generate_entities(input_path: Path, output_path: Path, column: str) -> int:
    if not input_path.exists():
        print(f"Error: input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    df = pd.read_parquet(input_path, columns=[column])

    if column not in df.columns:
        print(f"Error: column '{column}' not found. Available columns: {list(df.columns)}", file=sys.stderr)
        sys.exit(1)

    # Drop missing values and duplicates, keep as strings
    uris = (
        df[column]
        .dropna()
        .astype(str)
        .drop_duplicates()
        .sort_values()
        .tolist()
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        for uri in uris:
            f.write(uri + "\n")

    print(f"Wrote {len(uris)} unique entity URIs to {output_path}")
    return len(uris)


def main():
    parser = argparse.ArgumentParser(description="Extract entity URIs for OWL2Vec* pre_entity_file")
    parser.add_argument("--input", type=Path, default=Path("./data/disease/disease.parquet"),
                         help="Path to the Open Targets disease.parquet file")
    parser.add_argument("--output", type=Path, default=Path("./cache/entities.txt"),
                         help="Path to write the entities.txt cache file")
    parser.add_argument("--column", type=str, default="code",
                         help="Column containing entity URIs")
    args = parser.parse_args()

    generate_entities(args.input, args.output, args.column)


if __name__ == "__main__":
    main()