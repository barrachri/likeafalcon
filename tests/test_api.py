"""
Test API.
"""

import json
import asyncio


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
    await asyncio.sleep(2)
    assert resp.status == 200
    data = await resp.json()
    assert "We got" in data['message']
