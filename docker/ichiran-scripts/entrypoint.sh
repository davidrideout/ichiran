#!/bin/bash

echo "Checking postgres server status..."
while : ; do
    pg_isready -h localhost > /dev/null && break;
    sleep 1;
done

echo "Postgres is ready, starting main container init."
init-all;

cd api
uvicorn --host 0.0.0.0 main:app
