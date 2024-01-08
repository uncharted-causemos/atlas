#!/usr/bin/env bash

# Usage:
# ./update_mappings.sh [ELASTICSEARCH INSTANCE HOST AND PORT] [INDEX] [NEW MAPPING JSON]
# Example Usage:
# ./update_mappings.sh 10.65.18.61:9200/ insight mappings/insight.json
# ./update_mappings.sh localhost:9200 insight mappings/insight.json

ES=$1
INDEX=$2
MAPPING=$3

curl -XPUT -H "Content-type: application/json" $ES/$INDEX/_mapping -d@$MAPPING