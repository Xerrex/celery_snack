#!/bin/sh

#redis
docker run --rm --name celerysnack_redis -p 6379:6379 redis:alpine3.11