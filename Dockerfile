FROM centos:7.7.1908
ARG VMC_VERSION=1.0.1-alpha2
ENV VMC_VERSION=${VMC_VERSION}

ENV TZ=Poland
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

LABEL org.label-schema.license="Apache-2.0" \
      org.label-schema.url="http://dsecure.me"\
      org.label-schema.vendor="DSecure.me" \
      org.label-schema.name="VMC"

COPY root /

RUN yum install -y epel-release; \
    yum -y update;\
    yum install -y python36 python36-devel mariadb-devel gcc nginx; \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone; \
    pip3.6 install vmcenter==${VMC_VERSION}; \
    yum clean all; \
    chmod g=u /etc/passwd; \
    vmc collectstatic --noinput --clear; \
    chmod +x /usr/bin/entrypoint;

EXPOSE 8080

USER 1001

ENTRYPOINT ["entrypoint"]
