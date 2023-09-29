### atlas
atlas provides schemas and mappings for World Modelers

#### Prerequisite

Setup a virtual environment (optional but recommended)
```
python -m venv .venv
source .venv/bin/activate
```
Install dependencies
```
pip install -r requirements.txt
```

#### Creating initial indices/mappings
```
ES=<host:port> python es_mapper.py <index_name1> <index_name2> ...
```


#### Remove indices/mappings
Note: This is default to run against localhost to avoid accidentally deleting important data.
```
python clean_indices.py <index_name1> <index_name2> ...
```

Specifying no index names will create/clean all of the indices.



#### Docker
The Dockerfile will create a base ElasticSearch image with the index-mappings.
```
docker build -t <image_name> .
```
