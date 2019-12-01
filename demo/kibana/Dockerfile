ARG ELK_VERSION
FROM docker.elastic.co/kibana/kibana:${ELK_VERSION}

RUN /usr/share/kibana/bin/kibana-plugin install https://github.com/bitsensor/elastalert-kibana-plugin/releases/download/1.1.0/elastalert-kibana-plugin-1.1.0-7.3.2.zip
