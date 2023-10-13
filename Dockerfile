# Set the base image to elasticsearch alpine
FROM elasticsearch:7.17.4

WORKDIR /usr/share/elasticsearch

RUN apt-get update
RUN apt install -y python3 python3-pip

# copy in support scripts
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/e1f115e4ca285c3c24e847c4dd4be955e0ed51c2/wait-for-it.sh /wait-for-it.sh
RUN chmod 777 /wait-for-it.sh

# install python dependencies
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy ingestor
ADD es_mapper.py es_mapper.py
ADD mappings mappings

# Set environment variables to run elasticsearch in single node mode
ENV xpack.security.enabled=false
ENV discovery.type=single-node

ENV ES=localhost:9200

USER elasticsearch
