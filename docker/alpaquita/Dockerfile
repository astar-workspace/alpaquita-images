FROM docker.io/busybox:1.34.1-glibc AS builder

ARG STDLIB
ARG VERSION
ARG RELEASE_X64
ARG RELEASE_AARCH64

WORKDIR /root

RUN ARCH=$(uname -m) && \
    if [ "$ARCH" = "x86_64" ]; then \
        RELEASE="${RELEASE_X64}"; \
    elif [ "$ARCH" = "aarch64" ]; then \
        RELEASE="${RELEASE_AARCH64}"; \
    else \
        echo "Unsupported architecture: $ARCH" && exit 1; \
    fi && \
    wget -O minirootfs.tar.gz http://packages.bell-sw.com/alpaquita/${STDLIB}/${VERSION}/releases/$ARCH/alpaquita-minirootfs-${VERSION}-$RELEASE-${STDLIB}-$ARCH.tar.gz && \
    mkdir /root/rootfs && \
    tar -xzf /root/minirootfs.tar.gz -C /root/rootfs

FROM scratch
COPY --from=builder /root/rootfs/ /
CMD ["/bin/sh"]
