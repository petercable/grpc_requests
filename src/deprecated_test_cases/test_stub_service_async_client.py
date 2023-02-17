from .app import app
from .helloworld_pb2 import _GREETER
from ..testcase import RealServerAsyncTestCase
from ...grpc_requests import StubAsyncClient


class StubServiceClientTestCase(RealServerAsyncTestCase):
    reset_descriptor_pool = False
    app = app
    service = 'helloworld.Greeter'

    async def test_unary_unary_request(self):
        client = StubAsyncClient(self.default_endpoint, [_GREETER])
        svc = await client.service(self.service)
        request = {'name': "sinsky"}

        result = await svc.SayHello(request)

        self.assertIsInstance(result, dict)
        self.assertEqual(result.get('message'), 'Hello sinsky!')
        await client._channel.close()

    async def test_unary_stream_request(self):
        client = StubAsyncClient(self.default_endpoint, [_GREETER])
        svc = await client.service(self.service)
        request = {'name': "sinsky"}

        _results = await svc.SayHelloGroup(request)

        results = [x async for x in _results]
        self.assertEqual(4, len(results))
        names = ['a', 'b', 'c', 'd']

        for result, name in zip(results, names):
            self.assertIsInstance(result, dict)
            self.assertTrue(name in result.get('message'))
        await client._channel.close()

    async def test_stream_stream_request(self):
        client = StubAsyncClient(self.default_endpoint, [_GREETER])
        svc = await client.service(self.service)

        names = ['sinsky', 'summer', 'wone']
        _results = await svc.SayHelloOneByOne(({"name": name} for name in names))

        results = [x async for x in _results]
        self.assertEqual(len(names), len(results))

        for result, name in zip(results, names):
            self.assertIsInstance(result, dict)
            self.assertTrue(name in result.get('message'))
        await client._channel.close()

    async def test_success_request(self):
        client = StubAsyncClient(self.default_endpoint, [_GREETER])
        svc = await client.service(self.service)
        names = ['sinsky', 'summer', 'wone']
        result = await svc.HelloEveryone(({"name": name} for name in names))
        self.assertIsInstance(result, dict)
        self.assertTrue(f"{names}" in result.get('message', ''))
        await client._channel.close()
