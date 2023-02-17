import multiprocessing
import pytest
import time

from ..grpc_requests.client import Client
from .test_servers.helloworld_server import HelloWorldServer

"""
Test cases for reflection based client
"""

def helloworld_server_starter():
    server = HelloWorldServer('50051')
    server.serve()

@pytest.fixture(scope="module")
def helloworld_server():
    helloworld_server_process = multiprocessing.Process(target=helloworld_server_starter)
    helloworld_server_process.start()
    time.sleep(1)
    yield
    helloworld_server_process.terminate()


@pytest.fixture(scope="module")
def helloworld_reflection_client():
    try:
        client = Client.get_by_endpoint('localhost:50051')
        yield client
    except:  # noqa: E722
        pytest.fail("Could not connect to local HelloWorld server")


def test_unary_unary(helloworld_server, helloworld_reflection_client):
    response = helloworld_reflection_client.request('helloworld.Greeter', 'SayHello', {"name": "sinsky"})
    assert type(response) == dict
    assert response == {"message": "Hello, sinsky!"}

def test_unary_stream(helloworld_server, helloworld_reflection_client):
    name_list = ["sinsky", "viridianforge", "jack", "harry"]
    responses = helloworld_reflection_client.request(
        'helloworld.Greeter',
        'SayHelloGroup',
        {"name": "".join(name_list)}
    )
    assert all(type(response) == dict for response in responses)
    for response, name in zip(responses, name_list):
        assert response == {"message": f"Hello, {name}!"}

def test_stream_unary(helloworld_server, helloworld_reflection_client):
    name_list = ["sinsky", "viridianforge", "jack", "harry"]
    response = helloworld_reflection_client.request(
        'helloworld.Greeter',
        'HelloEveryone',
        [{"name": name} for name in name_list]
    )
    assert type(response) == dict
    assert response == {'message': f'Hello, {" ".join(name_list)}!'}

def test_stream_stream(helloworld_server, helloworld_reflection_client):
    name_list = ["sinsky", "viridianforge", "jack", "harry"]
    responses = helloworld_reflection_client.request(
        'helloworld.Greeter',
        'SayHelloOneByOne',
        [{"name": name} for name in name_list]
    )
    assert all(type(response) == dict for response in responses)
    for response, name in zip(responses, name_list):
        assert response == {"message": f"Hello, {name}!"}
