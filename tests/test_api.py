import json


async def test_no_data(cli):
    resp = await cli.post('/v1/json')
    assert resp.status == 400
    data = await resp.json()
    assert 'Error inside' in data['message']


async def test_empty_json(cli):
    resp = await cli.post('/v1/json', data="{}")
    assert resp.status == 400
    data = await resp.json()
    assert 'Empty json.' in data['message']


async def test_save_message(cli):
    data = {"message": "This is a secret message"}
    resp = await cli.post('/v1/json', data=json.dumps(data))
    assert resp.status == 200
    data = await resp.json()
    assert "We got" in data['message']


async def test_query_wrong_method(cli):
    resp = await cli.post('/query')
    assert resp.status == 405


async def test_query(cli):
    resp = await cli.get('/query')
    assert resp.status == 200
    data = await resp.json()
    assert "We got" in data['data']


async def test_query_with_params(cli):
    limit = 20
    offset = 30
    resp = await cli.get(f'/query?limit={limit}&offset={offset}')
    assert resp.status == 200
    data = await resp.json()
    assert data['limit'] == limit
    assert data['offset'] == offset

async def test_query_wrong_params(cli):
    limit = "hello"
    offset = 30
    resp = await cli.get(f'/query?limit={limit}&offset={offset}')
    assert resp.status == 400


async def test_query_with_params(cli):
    limit = 20
    offset = 30
    resp = await cli.get(f'/query?limit={limit}&offset={offset}')
    assert resp.status == 200
    data = await resp.json()
    assert data['limit'] == limit
    assert data['offset'] == offset
