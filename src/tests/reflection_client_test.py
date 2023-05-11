import logging
import pytest

from ..grpc_requests.client import Client
from google.protobuf.json_format import ParseError

"""
Test cases for reflection based client
"""

logger = logging.getLogger('name')

@pytest.fixture(scope="module")
def helloworld_reflection_client():
    try:
        client = Client.get_by_endpoint('localhost:50051')
        yield client
    except:  # noqa: E722
        pytest.fail("Could not connect to local HelloWorld server")


def test_unary_unary(helloworld_reflection_client):
    response = helloworld_reflection_client.request('helloworld.Greeter', 'SayHello', {"name": "sinsky"})
    assert type(response) == dict
    assert response == {"message": "Hello, sinsky!"}

def test_empty_body_request(helloworld_reflection_client):
    response = helloworld_reflection_client.request('helloworld.Greeter', 'SayHello', {})
    logger.warning(f"Response: {response}")
    assert type(response) == dict

def test_nonexistent_service(helloworld_reflection_client):
    with pytest.raises(ValueError):
        helloworld_reflection_client.request('helloworld.Speaker', 'SingHello', {})

def test_nonexistent_method(helloworld_reflection_client):
    with pytest.raises(ValueError):
        helloworld_reflection_client.request('helloworld.Greeter', 'SayGoodbye', {})

def test_unsupported_argument(helloworld_reflection_client):
    with pytest.raises(ParseError):
        helloworld_reflection_client.request('helloworld.Greeter', 'SayHello', {"foo": "bar"})

def test_unary_stream(helloworld_reflection_client):
    name_list = ["sinsky", "viridianforge", "jack", "harry"]
    responses = helloworld_reflection_client.request(
        'helloworld.Greeter',
        'SayHelloGroup',
        {"name": "".join(name_list)}
    )
    assert all(type(response) == dict for response in responses)
    for response, name in zip(responses, name_list):
        assert response == {"message": f"Hello, {name}!"}

def test_stream_unary(helloworld_reflection_client):
    name_list = ["sinsky", "viridianforge", "jack", "harry"]
    response = helloworld_reflection_client.request(
        'helloworld.Greeter',
        'HelloEveryone',
        [{"name": name} for name in name_list]
    )
    assert type(response) == dict
    assert response == {'message': f'Hello, {" ".join(name_list)}!'}

def test_stream_stream(helloworld_reflection_client):
    name_list = ["sinsky", "viridianforge", "jack", "harry"]
    responses = helloworld_reflection_client.request(
        'helloworld.Greeter',
        'SayHelloOneByOne',
        [{"name": name} for name in name_list]
    )
    assert all(type(response) == dict for response in responses)
    for response, name in zip(responses, name_list):
        assert response == {"message": f"Hello, {name}!"}

def test_reflection_service_client(helloworld_reflection_client):
    svc_client = helloworld_reflection_client.service('helloworld.Greeter')
    method_names = svc_client.method_names
    assert method_names == ('SayHello', 'SayHelloGroup', 'HelloEveryone', 'SayHelloOneByOne')

def test_reflection_service_client_invalid_service(helloworld_reflection_client):
    with pytest.raises(ValueError):
        helloworld_reflection_client.service('helloWorld.Singer')
