import os
import logging
from elasticsearch import Elasticsearch
import json
from smart_open import open

FORMAT = "%(asctime)-25s %(levelname)-8s %(message)s"
logging.basicConfig(format=FORMAT)
logger = logging.getLogger("es_mapper")
logger.setLevel(20)


def scan_directory(directory):
    """
    Returns absolute path of json files
    """
    mapping_files = []
    for f in os.listdir(directory):
        if not f.endswith("json"):
            continue
        mapping_files.append(os.path.join(directory, f))
    return mapping_files


def create_index(client, index_name, index_mappings):
    """
    Create index, returns status 400 if already exist
    """
    settings = {
        "index.number_of_shards": 1,
        "index.number_of_replicas": 0,
        "analysis": {
            "analyzer": {
                "concept-text": {
                    "type": "pattern",
                    "pattern": "[_/]",
                    "lowercase": True
                }
            }
        }
    }

    response = client.indices.create(
        index=index_name,
        body={"mappings": index_mappings, "settings": settings},
        ignore=400
    )
    if "error" in response:
        status = response["status"]
        logger.info(f"\t{status}")
    else:
        logger.info(f"\t{response}")


if __name__ == "__main__":
    host = os.environ.get("HOST")
    port = os.environ.get("PORT")
    mappings = scan_directory("./mappings")

    if host == None or port == None:
        logger.error("ES host or port not specified")
        exit(-1)

    client = Elasticsearch(host, port=port)

    for mapping_file in mappings:
        index_name = mapping_file.split("/")[-1].split(".")[0]
        logger.info(f"Creating index {index_name}")

        with open(mapping_file, 'r') as F:
            content = F.read()
            content = json.loads(content)
            create_index(client, index_name, content)

        # indra is a template index used to instantiate new indices, in order to clone the index we need
        # to put it into a read-only state
        if index_name == "indra":
            logger.info("Setting indra to readonly")
            body = {
                "index": {
                    "blocks.write": True,
                    "blocks.read_only": True
                }
            }
            client.indices.put_settings(body, index_name)

