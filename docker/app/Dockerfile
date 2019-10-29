FROM geocodi/py-development-alpine

ARG USER_UID
ARG USER_GID
ARG DOCKER_USER

# ENV LANG ca_ES.utf8

RUN apk update && apk add --no-cache gcc musl-dev make
RUN apk update && apk add --no-cache postgresql-dev poppler-utils jpeg-dev zlib-dev

ENV LIBRARY_PATH=/lib:/usr/lib

ENV GDAL_LIBRARY_PATH=/usr/lib/libgdal.so

RUN addgroup -g $USER_GID -S $DOCKER_USER && adduser -u $USER_UID -S $DOCKER_USER -G $DOCKER_USER

RUN mkdir -p /app
RUN mkdir -p /docker
RUN mkdir /docker_data

ADD requirements*.txt /docker/
ADD docker/app/entrypoint.sh /docker/
ADD docker/app/bash.sh /docker/
RUN chmod +x /docker/*.sh

ADD docker/app/bash.sh /bin/
RUN chmod +x /bin/bash.sh

RUN pip3 install --no-cache-dir -r /docker/requirements.txt
RUN if [ -n "$EXTRA_REQUIREMENTS" -a -f "/docker/requirements-$EXTRA_REQUIREMENTS.txt" ]; then pip3 install --no-cache-dir -r "/docker/requirements-$EXTRA_REQUIREMENTS.txt"; fi

# RUN apk rm postgresql-dev jpeg-dev zlib-dev

WORKDIR /app

ENTRYPOINT ["/bin/sh", "/docker/entrypoint.sh"]
