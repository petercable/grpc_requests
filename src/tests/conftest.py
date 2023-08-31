import multiprocessing
import pytest
import time

from test_servers.helloworld.helloworld_server import HelloWorldServer


def helloworld_server_starter():
    server = HelloWorldServer('50051')
    server.serve()

@pytest.fixture(scope="session", autouse=True)
def helloworld_server():
    helloworld_server_process = multiprocessing.Process(target=helloworld_server_starter)
    helloworld_server_process.start()
    time.sleep(1)
    yield
    helloworld_server_process.terminate()
