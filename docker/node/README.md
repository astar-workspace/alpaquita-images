# What is Node.js?

> Node.js is a cross-platform, open-source JavaScript runtime environment that can run on Windows, Linux, Unix, macOS, and more. Node.js runs on the V8 JavaScript engine, and executes JavaScript code outside a web browser.
> 
> Node.js lets developers use JavaScript to write command line tools and for server-side scripting. The ability to run JavaScript code on the server is often used to generate dynamic web page content before the page is sent to the user's web browser. Consequently, Node.js represents a "JavaScript everywhere" paradigm, unifying web-application development around a single programming language, as opposed to using different languages for the server- versus client-side programming. 

Quote from [Wikipedia Node.js Article](https://en.wikipedia.org/wiki/Node.js)

### What is included in this image?

- Node.js
- NPM
- Yarn

# Latest tags

## 20 (LTS)
- `20.18.0-alpaquita-stream-glibc`
- `20.18.0-alpaquita-stream-musl`

Aliases:
- `20-alpaquita-stream-glibc`
- `20-alpaquita-stream-musl`

Aliases:
- `lts-alpaquita-stream-glibc`
- `lts-alpaquita-stream-musl`

# Node.js release cycle

![NodeJS Release Cycle](https://i.ibb.co/dmy50JD/schedule.png)

## What is Alpaquita Linux?

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

## License

- Alpaquita Linux is licensed under the [Alpaquita Linux EULA](https://docs.bell-sw.com/alpaquita-linux/latest/legal/eula/).
- The `Dockerfile` used to build this image is licensed under the MIT License. Note that this refers to the `Dockerfile` itself, not the resulting container image.
- [Node.js license](https://github.com/nodejs/node/blob/main/LICENSE)

## Reference

- [Alpaquita Linux Homepage](https://bell-sw.com/alpaquita-linux/)
- [Having issues with Alpaquita Linux?](https://github.com/bell-sw/Alpaquita/issues)
- [Having issues with Node.js?](https://github.com/nodejs/node/issues)
- [Having issues with this container?](https://github.com/astarivi/alpaquita-images/issues)
- [Base Alpaquita Linux container](https://hub.docker.com/r/astarivi/alpaquita)
- [Node.js Dockerfile](https://github.com/astarivi/alpaquita-images/blob/main/docker/node/Dockerfile)
- [Node.js 20 APKBUILD file](https://github.com/astarivi/alpaquita-images/blob/main/aports/universe/node20/APKBUILD)