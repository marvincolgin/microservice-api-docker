# Layered Microservice APIs, written in Python and deployed in Docker

## Source Files

```
./api/__init__.py
./tests/test_index.py
```

## Testing

```
python -m pytest .\tests\test_index.py
```

## Building


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

### Docker

```
docker build --no-cache .

docker-compose up --build
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
