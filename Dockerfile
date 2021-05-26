FROM debian:buster-20210329-slim as builder

ARG VMC_VERSION=1.1-RC-2
ENV VMC_VERSION=${VMC_VERSION}

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apt-get update ; \
    apt-get install --no-install-recommends -y \
                   curl=7.64.0-4+deb10u2 \
                   libssl-dev=1.1.1d-0+deb10u6 \
                   python3=3.7.3-1 \
                   python3-pip=18.1-5 \
                   python3-dev=3.7.3-1 \
                   python3-distutils=3.7.3-1 \
                   python3-venv=3.7.3-1 \
                   build-essential=12.6; \
    python3 -m venv /opt/vmc;

RUN curl https://sh.rustup.rs -sSf | sh -s -- -y

ENV PATH="/root/.cargo/bin:${PATH}"
ENV PATH="/opt/vmc/bin:$PATH"

RUN pip3 install --no-cache-dir vmcenter==${VMC_VERSION}


FROM debian:buster-20210329-slim

ENV TZ=Poland
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV VMC_VERSION=${VMC_VERSION}
ENV PATH="/opt/vmc/bin:$PATH"


LABEL org.label-schema.schema-version="1.1-RC-2" \
      org.label-schema.license="Apache-2.0" \
      org.label-schema.url="https://dsecure.me"\
      org.label-schema.vendor="DSecure.me" \
      org.label-schema.name="VMC"

COPY root /
COPY --from=builder /opt/vmc /opt/vmc

RUN apt-get update; \
    apt-get install --no-install-recommends -y \
                       python3=3.7.3-1 \
                       python3-distutils=3.7.3-1 \
                       nginx=1.14.2-2+deb10u3; \
    mkdir -p /usr/share/vmc/static /usr/share/vmc/scans; \
    vmc collectstatic --noinput --clear; \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone; \
    rm -rf /var/lib/apt/lists/*; \
    chmod g=u /etc/passwd /usr/share/vmc; \
    chmod +x /usr/bin/entrypoint;


EXPOSE 8080

USER 1001

ENTRYPOINT ["entrypoint"]
