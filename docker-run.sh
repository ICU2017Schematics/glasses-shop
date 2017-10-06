#!/bin/sh

cat ./docker-compose.yml | envsubst | docker-compose -f - up
