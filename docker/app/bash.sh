#!/usr/bin/env sh

if [ -z "$1" ]
  then
    exec /usr/bin/gosu "$DOCKER_USER" "/bin/sh"
else
    exec /usr/bin/gosu "$DOCKER_USER" "$@"
fi
