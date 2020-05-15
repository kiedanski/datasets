#!/bin/bash

URL="https://www.ausgrid.com.au/-/media/Documents/Data-to-share/Solar-home-electricity-data/Solar-home-half-hour-data---1-July-2012-to-30-June-2013.zip"
OUT="data/solar_data_2012_2013.zip"

if [[ ! -f "$OUT" ]]; then
    wget "$URL" -q --show-progress -O "$OUT"
    unzip "$OUT" -d "data/"
else
    echo "File already exists"
fi

