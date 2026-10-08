#!/usr/bin/env bash
# Download the IMDb non-commercial datasets into data/imdb/
set -euo pipefail
DEST="$(dirname "$0")/../data/imdb"
mkdir -p "$DEST"
for f in name.basics title.akas title.basics title.crew title.episode title.principals title.ratings; do
  echo "Downloading $f ..."
  curl -fsSL "https://datasets.imdbws.com/$f.tsv.gz" -o "$DEST/$f.tsv.gz"
done
echo "Done."
