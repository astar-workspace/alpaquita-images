FROM docker.io/bellsoft/alpaquita-linux-base:stream-glibc AS builder

ARG STDLIB
ARG VERSION
ARG RELEASE_X64
ARG RELEASE_AARCH64

WORKDIR /root

RUN apk add wget && \
    ARCH=$(uname -m) && \
    if [ "$ARCH" = "x86_64" ]; then \
        RELEASE="${RELEASE_X64}"; \
    elif [ "$ARCH" = "aarch64" ]; then \
        RELEASE="${RELEASE_AARCH64}"; \
    else \
        echo "Unsupported architecture: $ARCH" && exit 1; \
    fi && \
    wget -O minirootfs.tar.gz https://packages.bell-sw.com/alpaquita/${STDLIB}/${VERSION}/releases/$ARCH/alpaquita-minirootfs-${VERSION}-$RELEASE-${STDLIB}-$ARCH.tar.gz && \
    mkdir /root/rootfs && \
    tar -xzf /root/minirootfs.tar.gz -C /root/rootfs

FROM scratch
COPY --from=builder /root/rootfs/ /
WORKDIR /root
CMD ["/bin/sh"]
