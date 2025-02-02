#!/bin/bash

echo "Checking postgres server status..."
while : ; do
    pg_isready -h localhost > /dev/null && break;
    sleep 1;
done

echo "Postgres is ready, starting main container init."
init-all;

cd api
uvicorn main:app
