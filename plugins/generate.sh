#!/usr/bin/env bash

FILE="./plugins.lst"

rm *.json
rm *.ttl

while IFS= read -r line; do
    echo "Processing plugin: $line"
    NAME=$(lv2info $line | grep "Name" -m 1 | cut -d ':' -f 2 | awk '{$1=$1};1')
    lv2info -p "$NAME.ttl" $line
    ttl2jsonld "$NAME.ttl" > "$NAME.json"
done < "$FILE"
