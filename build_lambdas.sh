#!/bin/bash

FUNCTIONS=("create" "get" "cache")

for i in "${!FUNCTIONS[@]}"; do
    echo "Building $FOLDER..."
    FOLDER=${FUNCTIONS[$i]}
    mkdir src/events/$FOLDER/build

    case "$FOLDER" in
    "create")
        cp src/events/$FOLDER/validators.py src/events/$FOLDER/insert_event_handler.py src/events/$FOLDER/build
        ;;
    "get")
        cp src/events/$FOLDER/get_events_handler.py src/events/$FOLDER/build
        ;;
    "cache")
         cp src/events/$FOLDER/get_redis_events_handler.py src/events/$FOLDER/build
        ;;
    *)
        echo "unknown folder"
        ;;
    esac

    cp .env src/events/$FOLDER/build
    pip install -r src/events/$FOLDER/requirements.txt \
        --platform manylinux2014_x86_64 \
        --target src/events/$FOLDER/build \
        --implementation cp \
        --python-version 3.11 \
        --only-binary=:all:

    cd src/events/$FOLDER/build

    zip -r ../../../../${FOLDER}_function.zip .
    cd ../../../../

done

echo "Finished building lambda zips"