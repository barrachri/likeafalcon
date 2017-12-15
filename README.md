# LikeaFalcon app
[![Build Status](https://travis-ci.org/barrachri/likeafalcon.svg?branch=pyup-config)](https://travis-ci.org/barrachri/likeafalcon)
[![codecov](https://codecov.io/gh/barrachri/likeafalcon/branch/master/graph/badge.svg)](https://codecov.io/gh/barrachri/likeafalcon)
[![Updates](https://pyup.io/repos/github/barrachri/likeafalcon/shield.svg)](https://pyup.io/repos/github/barrachri/likeafalcon/)

## Intro
this

## Requirements

Python 3.6.3

## How to test it
```python
make run-services
pip install tox
tox
make stop-services
```
## How to run it
```python
docker-compose up
```

The service is then reachable at `http://localhost:8080`.

## Endpoints available

### /v1/json

Accept post request with a json body.
The content will be fired to the event stream and then saved inside the database.

### /query?limit={10}&offset={0}

Return json body with a list of events actually stored inside the database.
You can specify an offset and limit, by default they are 0 and 10.

### /ws

Connect to the websocket and receive in real-time the event sent to `/v1/json`.

### /

A html web page that offers a connection to the `/ws` endpoint (websocket).
You will see in real-time the event sent to `/v1/json`.

## To-Do

1. Improve coverage to ~100% (basically add test for the websockets)
