import os
import sys
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
    mappings = [mapping.split("/")[-1] for mapping in scan_directory("./mappings")]
    client = Elasticsearch([ES])


    if len(sys.argv) > 1:
        indices = sys.argv[1:]
        indices = [mapping_file + ".json" for mapping_file in indices]
        print(indices)
        for json_file in indices:
            if json_file not in mappings:
                logger.error(f"JSON file {json_file} does not exist")
                exit(-1)
        mappings = indices

    # Clean out defined mappings
    for mapping_file in mappings:
        index_name = mapping_file.split(".")[0]

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


    if len(sys.argv) == 1:
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
