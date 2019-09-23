# Layered Microservice APIs, written in Python and deployed in Docker

This project is an example of a layered set of APIs, which expose a single public API and subsequently make many calls to sub-apis to accomplish a goal. This API is then packaged up as a Docker container, which can be spooled up for handling requests.

This example is written in Python and uses Flask for HTTP operations. The underlying data-structures utilize my library QuinnStruct, to provide BinarySearchTree, HashTable and Link List (hashtable collisions). 

On ```GET /```, the API will request X random integer values via ```GET /generate```, it will then ```POST /sort``` the list of integers to be inserted into a binary-search-tree and then perform a ```IN_ORDER``` traversal of the tree to return the sorted results. In order for the binary-search-tree to compare each nearly inserted value, it will make a ```GET /comparison``` to compare the two values.


## Source Files

```
./api/__init__.py
./tests/test_index.py
```

## Testing

```
python -m pytest .\tests\test_index.py
```
NOTE: Requires a copy of the API running on http://127.0.0.1:5000
@TODO: Use fixture to remove this dependancy

## Building

### Docker

```
docker-compose build

docker-compose up
```

## Running

### Flask

Windows
```
cd $REPO_DIR

set FLASK_APP=api
set FLASK_ENV=development

flask run
```

Linux
```
cd $REPO_DIR
export FLASK_APP=api; flask run
```

### Python Direct
```
cd $REPO_DIR
python ./src/index.py --port 5000
```

## API

### GET /

Main public facing API, ```GET /``` will return a JSON payload containing a numerically sorted list of integer values.

Performs ```GET /generate``` to obtain a random list of integers, validates the payload, then sends this JSON payload to ```POST /sort```


```
http GET :5000/
```
```
{
    "count": 5,
    "values": [
        "2",
        "14",
        "61",
        "907",
        "994"
    ]
}
```

### GET /generate

```
http GET :5000/generate
```
```
{
    "count": 5,
    "values": [
        {
            "name": "915",
            "value": 1
        },
        {
            "name": "283",
            "value": 1
        },
        ...
        {
            "name": "350",
            "value": 1
        },
        {
            "name": "69",
            "value": 1
        },
        {
            "name": "78",
            "value": 1
        }
    ]
}
```

### POST /sort

```
cat sort.json | http POST :5000/sort
```
```
{
    "count": 5,
    "values": [
        "69",
        "78",
        "283",
        "350",
        "915"
    ]
}
```
sort.json
```
{
  "count": 5,
  "values": [
    {
      "name": "915",
      "value": 1
    },
    {
      "name": "283",
      "value": 1
    },
    {
      "name": "350",
      "value": 1
    },
    {
      "name": "69",
      "value": 1
    },
    {
      "name": "78",
      "value": 1
    }
  ]
}
```

### GET /compare?val1=X&val2=Y&cs=9

```
http GET :5000/compare val1==1 val2==10 cs==1
```
```
{
    "result": true
}
```
