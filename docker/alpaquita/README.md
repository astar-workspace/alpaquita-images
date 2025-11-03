# What is Alpaquita Linux?

Alpaquita Linux is a lightweight operating system optimized for the deployment of cloud native applications. Based on Alpine Linux, it offers the flexibility of choosing between `glibc` and `musl` for the standard C library (`stdlib`) implementation.


>It is an optimal solution for running applications with various workloads >and is characterized by
>
> - Userspace binaries protection
> - Four malloc implementations in total
> - Optimized standard C library implementation ‘musl perf’, both small and >performant
> - Base image size of 3.22MB, which is perfect for running small and performant containers
> - Docker and QEMU support
>
> Alpaquita Linux is developed and maintained by [BellSoft](https://bell-sw.com).

Quote from [bellsoft/alpaquita-linux-base](https://hub.docker.com/r/bellsoft/alpaquita-linux-base)

# Latest tags

## 23 (LTS)
- `23-glibc-2.1`
- `23-musl-2.1`

Aliases:
- `23-glibc`
- `23-musl`

Aliases:
- `lts-glibc`
- `lts-musl`

## stream
- `stream-glibc-251102`
- `stream-musl-251102`

Aliases:
- `stream-glibc`
- `stream-musl`

`latest` is `stream-musl`

## Why another Alpaquita Linux container?

While BellSoft distributes the [alpaquita-linux-base container](https://hub.docker.com/r/bellsoft/alpaquita-linux-base), their versioning scheme may not align with certain workflows.

This container provides a consistent and up-to-date versioning scheme for Alpaquita Linux to address this gap.

## License

- Alpaquita Linux is licensed under the [Alpaquita Linux EULA](https://docs.bell-sw.com/alpaquita-linux/latest/legal/eula/)

## Reference

- [Alpaquita Linux Homepage](https://bell-sw.com/alpaquita-linux/)
- [Having issues with Alpaquita Linux?](https://github.com/bell-sw/Alpaquita/issues)
- [Having issues with this container?](https://github.com/astarivi/alpaquita-images/issues)
- [Version repository](https://github.com/astarivi/alpaquita-images/blob/main/docker/alpaquita/VERSIONS.md)
- [Universal Dockerfile](https://github.com/astarivi/alpaquita-images/blob/main/docker/alpaquita/Dockerfile)