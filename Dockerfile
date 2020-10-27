FROM centos:7.8.2003 as builder

ARG VMC_VERSION=1.1-RC-1
ENV VMC_VERSION=${VMC_VERSION}


RUN yum install -y epel-release-7-11.noarch; \
    yum install -y python3-3.6.8-13.el7.x86_64 \
                   python3-devel-3.6.8-13.el7.x86_64 \
                   mariadb-devel-1:5.5.65-1.el7.x86_64 \
                   gcc-4.8.5-39.el7.x86_64; \
    python3 -m venv /opt/vmc; \
    yum clean all;

ENV PATH="/opt/vmc/bin:$PATH"

RUN pip3.6 install --no-cache-dir vmcenter==${VMC_VERSION}


FROM centos:7.8.2003

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

RUN yum install -y epel-release-7-11.noarch; \
    yum install -y python3-3.6.8-13.el7.x86_64 \
                   mariadb-devel-1:5.5.65-1.el7.x86_64 \
                   nginx-1:1.16.1-2.el7.x86_64; \
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
