FROM ubuntu

RUN apt-get update && \
    apt-get install -y \
        curl \
        tzdata \
        python-pip \
        postgresql-client && \
        rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip 

WORKDIR /opt/perfbrowser-cli

COPY ./requirements.txt /opt/perfbrowser-cli/requirements.txt
RUN pip install -r /opt/perfbrowser-cli/requirements.txt
