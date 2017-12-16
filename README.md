# LikeAFalcon app
[![Build Status](https://travis-ci.org/barrachri/likeafalcon.svg?branch=pyup-config)](https://travis-ci.org/barrachri/likeafalcon)
[![codecov](https://codecov.io/gh/barrachri/likeafalcon/branch/master/graph/badge.svg)](https://codecov.io/gh/barrachri/likeafalcon)
[![Updates](https://pyup.io/repos/github/barrachri/likeafalcon/shield.svg)](https://pyup.io/repos/github/barrachri/likeafalcon/)

![falcon meme](http://s2.quickmeme.com/img/a8/a878a7df8054f0c4d15fd5523746e3727eb45d593ecaea77b9729adbbc571782.jpg "Falcon meme!")


## Intro
`LikeAFalcone` is an event driven system, receives an event, the event is then sent to a [NATS Stream](https://nats.io/documentation/streaming/nats-streaming-intro/).

After that watchers will receive notifications depending from the queue in which the event has been written, in this case `like.a.falcon`.

The watcher will then save the event inside a db.

You can access a real-time stream using websockets (`/ws`) or query the db for the events stored (`/query`).

This project uses [rampante](https://github.com/barrachri/rampante) a small collection of helpers to work with streams and aiohttp.

Main parts of this app are:

* app/api.py

    Create new events and query the db

* app/views.py

    Websocket page and websocket endpoint

* app/watchers.py

    Watch for new events

## Requirements

Python 3.6.3

## How to test it
Tests are written using PyTest, there is also a linting part before running the tests using `flake8` and `isort`.

```python
make run-services
pip install tox
tox
make stop-services
```
## How to run it
```bash
docker-compose up -d
```

The service is then reachable at `http://localhost:8080`.

## Create tables
Remeber to run `create_db.py` just after you created the db.
Env vars (user, password, db name) has to be set inside `config.py`.
```python
python create_db.py
```

## How to stop it
```bash
docker-compose stop
```

## How to remove it
```bash
docker-compose rm
```

## Endpoints available

### `/v1/json`

Accept post request with a json body.
The content will be fired to the event stream and then saved inside the database.

### `/query?limit={10}&offset={0}`

Return json body with a list of events actually stored inside the database.
You can specify an offset and limit, by default they are 0 and 10.

### `/ws`

Connect to the websocket and receive in real-time the event sent to `/v1/json`.

### `/`

A html web page that offers a connection to the `/ws` endpoint (websocket).
You will see in real-time the event sent to `/v1/json`.

## To-Do

1. Improve coverage to ~100% (basically add test for the websockets)
