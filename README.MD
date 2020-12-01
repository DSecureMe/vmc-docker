![logo](https://dsecure.me/wp-content/uploads/2019/11/dSecure-1.png)

[![badge](https://images.microbadger.com/badges/image/dsecureme/vmc.svg)](https://hub.docker.com/r/dsecureme/vmc/) [![badge_ver](https://images.microbadger.com/badges/version/dsecureme/vmc.svg)](https://microbadger.com/images/dsecureme/vmc "Get your own version badge on microbadger.com") [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# Dockerfile links
* Latest version [Dockerfile](Dockerfile)

# What is VMC
**[VMC](https://github.com/DSecureMe/vmc)** (Vulnerability Management Center) is a platform created to make vulnerability management simple, easy and clean.

# Get this image
The recommended way to get the VMC Docker Image is to pull the prebuilt image from the [Docker Hub Registry](https://hub.docker.com/r/dsecureme/vmc).
```bash
$ docker pull dsecureme/vmc:latest
```
To use a specific version, you can pull a versioned tag. You can view the [list of available versions](https://hub.docker.com/r/dsecureme/vmc/tags/) in the Docker Hub Registry.
```bash
$ docker pull dsecureme/vmc:[TAG]
```
If you wish, you can also build the image yourself.

```bash
$ git clone  https://github.com/DSecureMe/vmc-docker.git
$ make build
```

You can also make using version parameter
```bash
$ make build v=[version number]
```

# Requirements
* docker
* make

# Credit
[VMC](https://github.com/DSecureMe/vmc)

[DSecure.me](https://dsecure.me)
