#!/bin/bash

cat images/manifest.yaml | yq e '.images[] | .image' - | while read -r image; do
    if [[ "$image" == "" ]]; then
        continue
    fi
    echo "Pulling image: $image"
    wget "$image" -nc -P images/
done