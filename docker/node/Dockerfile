ARG BASE_IMAGE=latest
FROM docker.io/astarivi/alpaquita:${BASE_IMAGE} AS builder

# Install build dependencies
RUN apk add --no-cache build-base pkgconf sudo abuild python3 libstdc++ &&\
    rm /usr/lib/python3.*/EXTERNALLY-MANAGED &&\
    python -m ensurepip --upgrade

# Allow build_user to run sudo without a password
RUN echo "build_user ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers &&\
    adduser -D build_user &&\
    addgroup build_user abuild

ARG NODE_PKG=node20

COPY ./${NODE_PKG} /build/nodejs
COPY ./npm /build/npm
COPY ./yarn /build/yarn

RUN chown -R build_user:abuild /build

USER build_user

# Build npm
WORKDIR /build/npm
RUN abuild-keygen -a -i -n &&\
    abuild deps &&\
    abuild -r

# Build yarn
WORKDIR /build/yarn
RUN abuild deps &&\
    abuild -r

# Build node last, as it takes the longest
WORKDIR /build/nodejs
RUN abuild deps &&\
    abuild -r

FROM docker.io/astarivi/alpaquita:${BASE_IMAGE}

WORKDIR /root
COPY --from=builder /home/build_user/packages/build /root
RUN cd */ &&\
    rm -f *-dev* *-doc* *-completion* &&\
    apk add --no-cache --allow-untrusted node*.apk &&\
    apk add --no-cache --allow-untrusted npm*.apk &&\
    apk add --no-cache --allow-untrusted yarn*.apk &&\
    rm -rf /root/*

CMD [ "node" ]