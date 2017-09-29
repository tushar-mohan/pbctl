FROM ubuntu

RUN apt-get update && \
    apt-get install -y \
        curl \
        netcat \
        tzdata \
        postgresql-client && \
        rm -rf /var/lib/apt/lists/*

WORKDIR /opt/perfbrowser-cli
