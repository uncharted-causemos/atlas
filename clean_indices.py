import os
from elasticsearch import Elasticsearch
import logging

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

ES = "http://localhost:9200"

if __name__ == "__main__":
    mappings = scan_directory("./mappings")
    client = Elasticsearch([ES])

    # Clean out defined mappings
    for mapping_file in mappings:
        index_name = mapping_file.split("/")[-1].split(".")[0]

        if client.indices.exists(index=index_name) == False:
            continue

        logger.info(f"Deleting index {index_name}")

        if index_name.startswith("indra"):
            body = {
                "index": {
                    "blocks.write": False,
                    "blocks.read_only": False 
                }
            }
            client.indices.put_settings(body, index_name)

        client.indices.delete(index=index_name)


    # Clean out dynamic, user created indices
    indices = client.indices.get("*").keys()
    for index_name in indices:

        if index_name.startswith("indra") or index_name.startswith("project"):
            logger.info(f"Deleting index {index_name}")
            body = {
                "index": {
                    "blocks.write": False,
                    "blocks.read_only": False 
                }
            }
            client.indices.put_settings(body, index_name)
            client.indices.delete(index=index_name)
