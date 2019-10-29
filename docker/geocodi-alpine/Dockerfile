FROM osgeo/gdal:alpine-small-latest as builder
	# apk add --no-cache \
	# gcc musl-dev libffi-dev openssl-dev
	# Build geos
	RUN apk add --no-cache make g++ musl-dev
	ARG GEOS_VERSION=3.7.1
	RUN mkdir -p /build_thirdparty/usr/lib
	RUN if test "${GEOS_VERSION}" != ""; then ( \
	    wget -q http://download.osgeo.org/geos/geos-${GEOS_VERSION}.tar.bz2 \
	    && tar xjf geos-${GEOS_VERSION}.tar.bz2  \
	    && rm -f geos-${GEOS_VERSION}.tar.bz2 \
	    && cd geos-${GEOS_VERSION} \
	    && ./configure --prefix=/usr --disable-static --disable-dependency-tracking \
	    && make -j$(nproc) \
	    && make install \
	    && cp -P /usr/lib/libgeos*.so* /build_thirdparty/usr/lib \
	    && for i in /build_thirdparty/usr/lib/*; do strip -s $i 2>/dev/null || /bin/true; done \
	    && cd .. \
	    && rm -rf geos-${GEOS_VERSION} \
	    ); fi


FROM osgeo/gdal:alpine-small-latest

# ADD https://github.com/tianon/gosu/releases/download/1.11/gosu-amd64 /usr/sbin/gosu
# RUN chmod +x /usr/sbin/gosu

RUN apk update && \
	apk add --no-cache \
	python3 python3-dev py-pip \
	gcc musl-dev libffi-dev openssl-dev \
    curl unzip libexif udev chromium chromium-chromedriver

COPY --from=builder  /build_thirdparty/usr/ /usr/

# Install gosu
RUN apk add \
  --no-cache \
  --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
  gosu

RUN pip3 install --no-cache-dir uwsgi selenium==3.141.0 watchdog

RUN apk del libffi-dev openssl-dev

CMD ["/bin/sh"]
