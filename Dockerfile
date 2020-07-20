FROM centos:7.7.1908 as builder

ARG VMC_VERSION=1.1-RC-1
ENV VMC_VERSION=${VMC_VERSION}


RUN yum install -y epel-release; \
    yum install -y python36 python36-devel mariadb-devel gcc; \
    python3 -m venv /opt/vmc;

ENV PATH="/opt/vmc/bin:$PATH"

RUN pip3.6 install --no-cache-dir vmcenter==${VMC_VERSION}


FROM centos:7.7.1908

ENV TZ=Poland
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV VMC_VERSION=${VMC_VERSION}
ENV PATH="/opt/vmc/bin:$PATH"


LABEL org.label-schema.schema-version="1.1-RC-1" \
      org.label-schema.license="Apache-2.0" \
      org.label-schema.url="http://dsecure.me"\
      org.label-schema.vendor="DSecure.me" \
      org.label-schema.name="VMC"

COPY root /
COPY --from=builder /opt/vmc /opt/vmc

RUN yum install -y epel-release; \
    yum -y update; \
    yum install -y python36 nginx; \
    mkdir -p /usr/share/vmc/static; \
    vmc collectstatic --noinput --clear; \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone; \
    yum clean all; \
    rm -rf /var/cache/yum; \
    chmod g=u /etc/passwd; \
    chmod +x /usr/bin/entrypoint;


EXPOSE 8080

USER 1001

ENTRYPOINT ["entrypoint"]
