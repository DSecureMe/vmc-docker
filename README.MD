![logo](https://dsecure.me/wp-content/uploads/2019/11/dSecure-1.png)

[![badge](https://images.microbadger.com/badges/image/dsecureme/vmc.svg)](https://hub.docker.com/r/dsecureme/vmc/) [![badge_ver](https://images.microbadger.com/badges/version/dsecureme/vmc.svg)](https://microbadger.com/images/dsecureme/vmc "Get your own version badge on microbadger.com") [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# Dockerfile links
* Latest version [Dockerfile](Dockerfile)

# What is VMC
**[VMC](https://github.com/DSecureMe/vmc)** (Vulnerability Management Center) is a platform created to make vulnerability management simple, easy and clean.

# How to use
## To run demo
Open demo folder and build (it may take couple minutes)
```
git submodule update --init --recursive
make build
make up
```
For now you must manually load dashboard config file to Kibana. Open Web GUI (default kibana port). Then go to _Management_ -> _Saved Objects_ -> Import and select _export.ndjson_

On port `:8080/admin` you can find VMC admin panel.
You log in there with following credentials `admin:adminadmin`
Go to Cves and then click on Import CVE (upper-right corner)

More guides will be published on [doc report](https://github.com/DSecureMe/vmcDocs) very soon

# Configuration files
All configs you may find in `demo/config/`

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
# Demo configuration file
Once build it will be in `/etc/vmc/`
In demo repo you can find it in `/demo/config/vmc/demo.yml`
```
#Redis
redis.url: redis://redis:6379/1

#Elastic Search
elasticsearch.hosts: ["http://elasticsearch:9200"]
elasticsearch.user: elastic
elasticsearch.password: kibana

#database
database.engine: django.db.backends.postgresql_psycopg2
database.name: vmc
database.user: user
database.password: password
database.host: postgres
database.port: 5432

# Queue
rabbitmq.username: vmc
rabbitmq.password: test_vmc
rabbitmq.host: rabbitmq
rabbitmq.port: 5672

# Secret
secret_key: "jk&e^6%5@^5!^1jq8#vd2g^@8w9g5#i_v*ho!#mx%y7%5fuz9%"
debug: true

# Admin Service Name
admin_service_name: admin
```


# Requirments
* docker
* docker compose
* make

# Credit
[VMC](https://github.com/DSecureMe/vmc)

[DSecure.me](https://dsecure.me)
