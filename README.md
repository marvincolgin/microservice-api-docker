# Layered Microservice APIs, written in Python and deployed in Docker



## API

### GET /

Main public facing API, ```GET /``` will return a JSON payload containing a numerically sorted list of integer values.

Performs ```GET /generate``` to obtain a random list of integers, validates the payload, then sends this JSON payload to ```POST /sort```


```
http GET :8000/


HTTP/1.0 200 OK
Content-Length: 318
Content-Type: application/json
Date: Sat, 21 Sep 2019 03:20:12 GMT
Server: Werkzeug/0.16.0 Python/3.7.4

{
    "count": 50,
    "values": [
        "2",
        "14",
        "50",
        "61",
        ...
        "907",
        "957",
        "969",
        "989",
        "994"
    ]
}
```

### GET /generate

```
http GET :8000/generate


HTTP/1.0 200 OK
Content-Length: 1266
Content-Type: application/json
Date: Sat, 21 Sep 2019 03:28:14 GMT
Server: Werkzeug/0.16.0 Python/3.7.4

{
    "count": 50,
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


HTTP/1.0 200 OK
Content-Length: 93
Content-Type: application/json
Date: Sat, 21 Sep 2019 03:51:00 GMT
Server: Werkzeug/0.16.0 Python/3.7.4

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


HTTP/1.0 200 OK
Content-Length: 21
Content-Type: application/json
Date: Sat, 21 Sep 2019 03:56:41 GMT
Server: Werkzeug/0.16.0 Python/3.7.4

{
    "result": true
}
```