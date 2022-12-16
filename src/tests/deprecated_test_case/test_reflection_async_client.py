from .app import app
from ..testcase import RealServerAsyncTestCase
from ...grpc_requests.aio import AsyncClient


class UnaryUnaryAsyncTestCase(RealServerAsyncTestCase):
    app = app
    service = 'helloworld.Greeter'
    method = 'SayHello'

    async def test_success_request(self):
        client = AsyncClient(self.default_endpoint)
        result = await client.unary_unary(self.service, self.method, {'name': "sinsky"})

        self.assertIsInstance(result, dict)
        self.assertEqual(result.get('message'), 'Hello sinsky!')
        await client._channel.close()

    async def test_not_support_service(self):
        client = AsyncClient(self.default_endpoint)
        not_support_service = 'notSupport'
        with self.assertRaises(ValueError) as context:
            await client.unary_unary(not_support_service, self.method, {'name': "sinsky"})
        exception_msg = f"{context.exception}"
        print(exception_msg)
        self.assertTrue(f"server doesn't support {not_support_service}" in exception_msg)
        for service in ('grpc.health.v1.Health', 'grpc.reflection.v1alpha.ServerReflection', 'helloworld.Greeter'):
            self.assertTrue(service in exception_msg)
        await client._channel.close()

    async def test_not_support_method(self):
        client = AsyncClient(self.default_endpoint)
        not_support_method = 'notSupport'
        with self.assertRaises(ValueError) as context:
            await client.unary_unary(self.service, not_support_method, {'name': "sinsky"})
        exception_msg = f"{context.exception}"
        print(exception_msg)
        self.assertTrue(f"{self.service} doesn't support {not_support_method} method" in exception_msg)
        for method in ('HelloEveryone', 'SayHello', 'SayHelloGroup', 'SayHelloOneByOne'):
            self.assertTrue(method in exception_msg)
        await client._channel.close()


class UnaryStreamAsyncTestCase(RealServerAsyncTestCase):
    app = app
    service = 'helloworld.Greeter'
    method = 'SayHelloGroup'

    async def test_success_request(self):
        client = AsyncClient(self.default_endpoint)
        _results = await client.unary_stream(self.service, self.method, {'name': "sinsky"})

        results = [x async for x in _results]
        # results = [x async for x in _results]

        print(results)
        self.assertEqual(4, len(results))
        names = ['a', 'b', 'c', 'd']

        for result, name in zip(results, names):
            self.assertIsInstance(result, dict)
            self.assertTrue(name in result.get('message'))
        await client._channel.close()

    async def test_not_support_service(self):
        client = AsyncClient(self.default_endpoint)
        not_support_service = 'notSupport'
        with self.assertRaises(ValueError) as context:
            await client.unary_stream(not_support_service, self.method, {'name': "sinsky"})
        exception_msg = f"{context.exception}"

        self.assertTrue(f"server doesn't support {not_support_service}" in exception_msg)
        for service in ('grpc.health.v1.Health', 'grpc.reflection.v1alpha.ServerReflection', 'helloworld.Greeter'):
            self.assertTrue(service in exception_msg)
        await client._channel.close()

    async def test_not_support_method(self):
        client = AsyncClient.get_by_endpoint(self.default_endpoint)
        not_support_method = 'notSupport'
        with self.assertRaises(ValueError) as context:
            await client.unary_stream(self.service, not_support_method, {'name': "sinsky"})
        exception_msg = f"{context.exception}"

        self.assertTrue(f"{self.service} doesn't support {not_support_method} method" in exception_msg)
        for method in ('HelloEveryone', 'SayHello', 'SayHelloGroup', 'SayHelloOneByOne'):
            self.assertTrue(method in exception_msg)
        await client._channel.close()


class StreamStreamAsyncTestCase(RealServerAsyncTestCase):
    app = app
    service = 'helloworld.Greeter'
    method = 'SayHelloOneByOne'

    async def test_success_request(self):
        client = AsyncClient(self.default_endpoint)
        names = ['sinsky', 'summer', 'wone']
        _results = await client.stream_stream(self.service, self.method, ({"name": name} for name in names))
        results = [x async for x in _results]

        self.assertEqual(len(names), len(results))

        for result, name in zip(results, names):
            self.assertIsInstance(result, dict)
            self.assertTrue(name in result.get('message'))
        await client._channel.close()

    async def test_not_support_service(self):
        client = AsyncClient(self.default_endpoint)
        not_support_service = 'notSupport'
        with self.assertRaises(ValueError) as context:
            await client.stream_stream(not_support_service, self.method, [{'name': "sinsky"}])
        exception_msg = f"{context.exception}"

        self.assertTrue(f"server doesn't support {not_support_service}" in exception_msg)
        for service in ('grpc.health.v1.Health', 'grpc.reflection.v1alpha.ServerReflection', 'helloworld.Greeter'):
            self.assertTrue(service in exception_msg)
        await client._channel.close()

    async def test_not_support_method(self):
        client = AsyncClient.get_by_endpoint(self.default_endpoint)
        not_support_method = 'notSupport'
        with self.assertRaises(ValueError) as context:
            await client.stream_stream(self.service, not_support_method, [{'name': "sinsky"}])
        exception_msg = f"{context.exception}"
        self.assertTrue(f"{self.service} doesn't support {not_support_method} method" in exception_msg)
        for method in ('HelloEveryone', 'SayHello', 'SayHelloGroup', 'SayHelloOneByOne'):
            self.assertTrue(method in exception_msg)

        await client._channel.close()


class StreamUnaryAsyncTestCase(RealServerAsyncTestCase):
    app = app
    service = 'helloworld.Greeter'
    method = 'HelloEveryone'

    async def test_success_request(self):
        client = AsyncClient(self.default_endpoint)
        names = ['sinsky', 'summer', 'wone']
        result = await client.stream_unary(self.service, self.method, ({"name": name} for name in names))
        self.assertIsInstance(result, dict)
        self.assertTrue(f"{names}" in result.get('message', ''))
        await client._channel.close()

    async def test_not_support_service(self):
        client = AsyncClient(self.default_endpoint)
        not_support_service = 'notSupport'
        with self.assertRaises(ValueError) as context:
            await client.stream_unary(not_support_service, self.method, [{'name': "sinsky"}])
        exception_msg = f"{context.exception}"

        self.assertTrue(f"server doesn't support {not_support_service}" in exception_msg)
        for service in ('grpc.health.v1.Health', 'grpc.reflection.v1alpha.ServerReflection', 'helloworld.Greeter'):
            self.assertTrue(service in exception_msg)
        await client._channel.close()

    async def test_not_support_method(self):
        client = AsyncClient(self.default_endpoint)
        not_support_method = 'notSupport'
        with self.assertRaises(ValueError) as context:
            await client.stream_unary(self.service, not_support_method, [{'name': "sinsky"}])
        exception_msg = f"{context.exception}"

        self.assertTrue(f"{self.service} doesn't support {not_support_method} method" in exception_msg)
        for method in ('HelloEveryone', 'SayHello', 'SayHelloGroup', 'SayHelloOneByOne'):
            self.assertTrue(method in exception_msg)
        await client._channel.close()
