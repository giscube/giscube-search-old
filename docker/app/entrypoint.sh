#!/usr/bin/env sh
set -e

exec /usr/bin/gosu $DOCKER_USER "$@"
