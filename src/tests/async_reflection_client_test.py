import logging
import pytest

from grpc_requests.aio import AsyncClient
from google.protobuf.json_format import ParseError

"""
Test cases for reflection based client
"""

logger = logging.getLogger('name')

@pytest.fixture(scope="module")
def helloworld_reflection_client():
    try:
        client = AsyncClient.get_by_endpoint('localhost:50051')
        yield client
    except:  # noqa: E722
        pytest.fail("Could not connect to local HelloWorld server")

@pytest.fixture(scope="module")
def client_tester_reflection_client():
    try:
        client = AsyncClient.get_by_endpoint('localhost:50051')
        yield client
    except:  # noqa: E722
        pytest.fail("Could not connect to local Test server")

@pytest.mark.asyncio
async def test_unary_unary(helloworld_reflection_client):
    response = await helloworld_reflection_client.request('helloworld.Greeter', 'SayHello', {"name": "sinsky"})
    assert isinstance(response, dict)
    assert response == {"message": "Hello, sinsky!"}

@pytest.mark.asyncio
async def test_empty_body_request(helloworld_reflection_client):
    response = await helloworld_reflection_client.request('helloworld.Greeter', 'SayHello', {})
    assert isinstance(response, dict)

@pytest.mark.asyncio
async def test_nonexistent_service(helloworld_reflection_client):
    with pytest.raises(ValueError):
        await helloworld_reflection_client.request('helloworld.Speaker', 'SingHello', {})

@pytest.mark.asyncio
async def test_nonexistent_method(helloworld_reflection_client):
    with pytest.raises(ValueError):
        await helloworld_reflection_client.request('helloworld.Greeter', 'SayGoodbye', {})

@pytest.mark.asyncio
async def test_unsupported_argument(helloworld_reflection_client):
    with pytest.raises(ParseError):
        await helloworld_reflection_client.request('helloworld.Greeter', 'SayHello', {"foo": "bar"})

@pytest.mark.asyncio
async def test_unary_stream(helloworld_reflection_client):
    name_list = ["sinsky", "viridianforge", "jack", "harry"]
    greeter = await helloworld_reflection_client.service('helloworld.Greeter')
    responses = [x async for x in await greeter.SayHelloGroup(
        [{"name": name} for name in name_list]
    )]
    assert all(isinstance(response, dict) for response in responses)
    for response, name in zip(responses, name_list):
        assert response == {"message": f"Hello, {name}!"}

@pytest.mark.asyncio
async def test_stream_unary(helloworld_reflection_client):
    name_list = ["sinsky", "viridianforge", "jack", "harry"]
    greeter = await helloworld_reflection_client.service('helloworld.Greeter')
    response = await greeter.HelloEveryone([{"name": name} for name in name_list])
    assert isinstance(response, dict)
    assert response == {'message': f'Hello, {" ".join(["sinsky", "viridianforge", "jack", "harry"])}!'}

@pytest.mark.asyncio
async def test_stream_stream(helloworld_reflection_client):
    name_list = ["sinsky", "viridianforge", "jack", "harry"]
    greeter = await helloworld_reflection_client.service('helloworld.Greeter')
    responses = [x async for x in await greeter.SayHelloOneByOne([{"name": name} for name in name_list])]
    assert all(isinstance(response, dict) for response in responses)
    for response, name in zip(responses, name_list):
        assert response == {"message": f"Hello {name}"}

@pytest.mark.asyncio
async def test_reflection_service_client(helloworld_reflection_client):
    svc_client = await helloworld_reflection_client.service('helloworld.Greeter')
    method_names = svc_client.method_names
    assert method_names == ('SayHello', 'SayHelloGroup', 'HelloEveryone', 'SayHelloOneByOne')

@pytest.mark.asyncio
async def test_reflection_service_client_invalid_service(helloworld_reflection_client):
    with pytest.raises(ValueError):
        await helloworld_reflection_client.service('helloWorld.Singer')
