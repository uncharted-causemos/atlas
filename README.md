### atlas
atlas provides schemas and mappings for World Modelers


#### Creating initial indices/mappings
```
ES=<host:port> python es_mapper.py <index_name1> <index_name2> ...
```


#### Creating initial indices/mappings
Note: This is default to run against localhost to avoid accidentally deleting important data.
```
python clean_indices.py <index_name1> <index_name2> ...
```

Specifying no index names will create/clean all of the indices.
