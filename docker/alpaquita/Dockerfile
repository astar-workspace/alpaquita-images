FROM docker.io/busybox:1.37.0-musl AS builder

ARG STDLIB
ARG VERSION
ARG RELEASE

WORKDIR /root

RUN ARCH=$(uname -m) && \
    wget -O minirootfs.tar.gz https://packages.bell-sw.com/alpaquita/${STDLIB}/${VERSION}/releases/$ARCH/alpaquita-minirootfs-${VERSION}-${RELEASE}-${STDLIB}-$ARCH.tar.gz && \
    mkdir /root/rootfs && \
    tar -xzf /root/minirootfs.tar.gz -C /root/rootfs

FROM scratch
COPY --from=builder /root/rootfs/ /
CMD ["/bin/sh"]
