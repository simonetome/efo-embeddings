#!/bin/bash

mkdir -p data
mkdir -p embeddings
mkdir -p cache


if [ ! -e data/efo_otar_slim.owl ]; then
    echo "Downloading EFO owl"
    wget https://github.com/EBISPOT/efo/releases/download/v3.88.0/efo_otar_slim.owl -P data
fi


if [ ! -e data/disease ]; then
    echo "Downloading disease info from OT release March 2026"
    rsync -rpltvz --delete rsync.ebi.ac.uk::pub/databases/opentargets/platform/26.03/output/disease data/.
fi