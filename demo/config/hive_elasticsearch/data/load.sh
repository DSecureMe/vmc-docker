#!/usr/bin/env bash

curl -XPUT 'http://localhost:9200/_snapshot/the_hive_backup' -H 'Content-Type: application/json' -d '{
    "type": "fs",
    "settings": {
        "location": "/test_data",
        "compress": true
    }
}'

curl -X POST 'http://localhost:9200/_snapshot/the_hive_backup/snapshot/_restore'
