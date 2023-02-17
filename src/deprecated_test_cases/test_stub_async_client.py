from .app import app
from .helloworld_pb2 import _GREETER
from ..testcase import RealServerAsyncTestCase
from ...grpc_requests.aio import StubAsyncClient


class UnaryUnaryTestCase(RealServerAsyncTestCase):
    reset_descriptor_pool = False
    app = app
    service = 'helloworld.Greeter'
    method = 'SayHello'

    def setUp(self):
        super(UnaryUnaryTestCase, self).setUp()

    async def test_success_request(self):
        client = StubAsyncClient(self.default_endpoint, [_GREETER])
        result = await client.unary_unary(self.service, self.method, {'name': "sinsky"})

        self.assertIsInstance(result, dict)
        self.assertEqual(result.get('message'), 'Hello sinsky!')
        await client._channel.close()

    async def test_not_support_service(self):
        client = StubAsyncClient(self.default_endpoint, [_GREETER])
        not_support_service = 'notSupport'
        with self.assertRaises(ValueError) as context:
            await client.unary_unary(not_support_service, self.method, {'name': "sinsky"})
        exception_msg = f"{context.exception}"
        print(exception_msg)
        self.assertTrue(f"server doesn't support {not_support_service}" in exception_msg)
        for service in ('helloworld.Greeter'):
            self.assertTrue(service in exception_msg)
        await client._channel.close()

    async def test_not_support_method(self):
        client = StubAsyncClient(self.default_endpoint, [_GREETER])
        not_support_method = 'notSupport'
        with self.assertRaises(ValueError) as context:
            await client.unary_unary(self.service, not_support_method, {'name': "sinsky"})
        exception_msg = f"{context.exception}"
        print(exception_msg)
        self.assertTrue(f"{self.service} doesn't support {not_support_method} method" in exception_msg)
        for method in ('HelloEveryone', 'SayHello', 'SayHelloGroup', 'SayHelloOneByOne'):
            self.assertTrue(method in exception_msg)
        await client._channel.close()


class UnaryStreamTestCase(RealServerAsyncTestCase):
    app = app
    service = 'helloworld.Greeter'
    method = 'SayHelloGroup'
    reset_descriptor_pool = False

    async def test_success_request(self):
        client = StubAsyncClient(self.default_endpoint, [_GREETER])
        _results = await client.unary_stream(self.service, self.method, {'name': "sinsky"})

        results = [x async for x in _results]
        self.assertEqual(4, len(results))
        names = ['a', 'b', 'c', 'd']

        for result, name in zip(results, names):
            self.assertIsInstance(result, dict)
            self.assertTrue(name in result.get('message'))
        await client._channel.close()

    async def test_not_support_service(self):
        client = StubAsyncClient(self.default_endpoint, [_GREETER])
        not_support_service = 'notSupport'
        with self.assertRaises(ValueError) as context:
            await client.unary_stream(not_support_service, self.method, {'name': "sinsky"})
        exception_msg = f"{context.exception}"
        # print(exception_msg)
        self.assertTrue(f"server doesn't support {not_support_service}" in exception_msg)
        for service in ('helloworld.Greeter',):
            self.assertTrue(service in exception_msg)
        await client._channel.close()

    async def test_not_support_method(self):
        client = StubAsyncClient(self.default_endpoint, [_GREETER])
        not_support_method = 'notSupport'
        with self.assertRaises(ValueError) as context:
            await client.unary_stream(self.service, not_support_method, {'name': "sinsky"})
        exception_msg = f"{context.exception}"
        # print(exception_msg)
        self.assertTrue(f"{self.service} doesn't support {not_support_method} method" in exception_msg)
        for method in ('HelloEveryone', 'SayHello', 'SayHelloGroup', 'SayHelloOneByOne'):
            self.assertTrue(method in exception_msg)
        await client._channel.close()


class StreamStreamTestCase(RealServerAsyncTestCase):
    app = app
    service = 'helloworld.Greeter'
    method = 'SayHelloOneByOne'
    reset_descriptor_pool = False

    async def test_success_request(self):
        client = StubAsyncClient(self.default_endpoint, [_GREETER])
        names = ['sinsky', 'summer', 'wone']
        _results = await client.stream_stream(self.service, self.method, ({"name": name} for name in names))

        results = [x async for x in _results]
        self.assertEqual(len(names), len(results))

        for result, name in zip(results, names):
            self.assertIsInstance(result, dict)
            self.assertTrue(name in result.get('message'))
        await client._channel.close()

    async def test_not_support_service(self):
        client = StubAsyncClient(self.default_endpoint, [_GREETER])
        not_support_service = 'notSupport'
        with self.assertRaises(ValueError) as context:
            await client.stream_stream(not_support_service, self.method, [{'name': "sinsky"}])
        exception_msg = f"{context.exception}"

        self.assertTrue(f"server doesn't support {not_support_service}" in exception_msg)
        for service in ('helloworld.Greeter',):
            self.assertTrue(service in exception_msg)
        await client._channel.close()

    async def test_not_support_method(self):
        client = StubAsyncClient(self.default_endpoint, [_GREETER])
        not_support_method = 'notSupport'
        with self.assertRaises(ValueError) as context:
            await client.stream_stream(self.service, not_support_method, [{'name': "sinsky"}])
        exception_msg = f"{context.exception}"

        self.assertTrue(f"{self.service} doesn't support {not_support_method} method" in exception_msg)
        for method in ('HelloEveryone', 'SayHello', 'SayHelloGroup', 'SayHelloOneByOne'):
            self.assertTrue(method in exception_msg)

        await client._channel.close()


class StreamUnaryTestCase(RealServerAsyncTestCase):
    app = app
    service = 'helloworld.Greeter'
    method = 'HelloEveryone'
    reset_descriptor_pool = False

    async def test_success_request(self):
        client = StubAsyncClient(self.default_endpoint, [_GREETER])
        names = ['sinsky', 'summer', 'wone']
        result = await client.stream_unary(self.service, self.method, ({"name": name} for name in names))
        self.assertIsInstance(result, dict)
        self.assertTrue(f"{names}" in result.get('message', ''))
        await client._channel.close()

    async def test_not_support_service(self):
        client = StubAsyncClient(self.default_endpoint, [_GREETER])
        not_support_service = 'notSupport'
        with self.assertRaises(ValueError) as context:
            await client.stream_unary(not_support_service, self.method, [{'name': "sinsky"}])
        exception_msg = f"{context.exception}"

        self.assertTrue(f"server doesn't support {not_support_service}" in exception_msg)
        for service in ('helloworld.Greeter',):
            self.assertTrue(service in exception_msg)
        await client._channel.close()

    async def test_not_support_method(self):
        client = StubAsyncClient(self.default_endpoint, [_GREETER])
        not_support_method = 'notSupport'
        with self.assertRaises(ValueError) as context:
            await client.stream_unary(self.service, not_support_method, [{'name': "sinsky"}])
        exception_msg = f"{context.exception}"
        print(exception_msg)
        self.assertTrue(f"{self.service} doesn't support {not_support_method} method" in exception_msg)
        for method in ('HelloEveryone', 'SayHello', 'SayHelloGroup', 'SayHelloOneByOne'):
            self.assertTrue(method in exception_msg)
        await client._channel.close()
