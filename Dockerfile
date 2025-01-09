ARG BASE_IMAGE

#trivy:ignore:AVD-DS-0001
FROM $BASE_IMAGE as base

RUN apt-get update \
    && apt-get dist-upgrade -y \
    && apt-get install -y --no-install-recommends netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

FROM base as install

ARG PACKAGE_TARBALL

COPY dist/$PACKAGE_TARBALL /

RUN python3 -m venv /opt/ddam \
    && /opt/ddam/bin/pip3 install /"$PACKAGE_TARBALL"

FROM base

COPY --from=install /opt/ddam /opt/ddam

ENV PATH=/opt/ddam/bin:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

RUN install -d -o nobody -m 0700 /run/exabgp

COPY docker-entrypoint.sh /docker-entrypoint.sh

USER nobody

ENV exabgp.tcp.bind=127.0.0.1
ENV exabgp.tcp.port=1790

HEALTHCHECK --interval=30s --timeout=2s \
  CMD /usr/bin/timeout 2 /usr/bin/nc -z 127.0.0.1 1790 || exit 1

ENTRYPOINT ["/docker-entrypoint.sh"]

# https://github.com/opencontainers/image-spec/blob/main/annotations.md
LABEL org.opencontainers.image.revision=${GIT_COMMIT_SHA}
