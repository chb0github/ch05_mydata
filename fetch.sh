#!/bin/zsh
set -e
set -o pipefail

url=${1:?no url provided}
mkdir -p data
# https://www.ncei.noaa.gov/data/global-summary-of-the-year/access/
curl -s "${url}" |
  sed -En 's/.*href="([^"]*)".*/\1/p'  |
    xargs printf "%s/%s\n" "${url}" |
    xargs -P 200 -n 100 wget -q -P data

find data/ -type f -name '*.csv' -print0 | xargs -0 -n 100 -P 20 tail -n +2 -q > data/combined.csv  
