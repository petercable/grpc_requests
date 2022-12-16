import unittest

from .app import app
from .helloworld_pb2 import _GREETER
from ..testcase import RealServerTestCase
from ...grpc_requests import StubClient


class UnaryUnaryTestCase(RealServerTestCase):
    reset_descriptor_pool = False
    app = app
    service = 'helloworld.Greeter'
    method = 'SayHello'

    def setUp(self):
        super(UnaryUnaryTestCase, self).setUp()

    def test_success_request(self):
        client = StubClient(self.default_endpoint, [_GREETER])
        result = client.unary_unary(self.service, self.method, {'name': "sinsky"})

        self.assertIsInstance(result, dict)
        self.assertEqual(result.get('message'), 'Hello sinsky!')
        client._channel.close()

    def test_not_support_service(self):
        client = StubClient(self.default_endpoint, [_GREETER])
        not_support_service = 'notSupport'
        with self.assertRaises(ValueError) as context:
            client.unary_unary(not_support_service, self.method, {'name': "sinsky"})
        exception_msg = f"{context.exception}"
        print(exception_msg)
        self.assertTrue(f"server doesn't support {not_support_service}" in exception_msg)
        for service in ('helloworld.Greeter'):
            self.assertTrue(service in exception_msg)
        client._channel.close()

    def test_not_support_method(self):
        client = StubClient(self.default_endpoint, [_GREETER])
        not_support_method = 'notSupport'
        with self.assertRaises(ValueError) as context:
            client.unary_unary(self.service, not_support_method, {'name': "sinsky"})
        exception_msg = f"{context.exception}"
        print(exception_msg)
        self.assertTrue(f"{self.service} doesn't support {not_support_method} method" in exception_msg)
        for method in ('HelloEveryone', 'SayHello', 'SayHelloGroup', 'SayHelloOneByOne'):
            self.assertTrue(method in exception_msg)
        client._channel.close()


class UnaryStreamTestCase(RealServerTestCase):
    app = app
    service = 'helloworld.Greeter'
    method = 'SayHelloGroup'
    reset_descriptor_pool = False

    def test_success_request(self):
        client = StubClient(self.default_endpoint, [_GREETER])
        _results = client.unary_stream(self.service, self.method, {'name': "sinsky"})

        results = [x for x in _results]
        print(results)
        self.assertEqual(4, len(results))
        names = ['a', 'b', 'c', 'd']

        for result, name in zip(_results, names):
            self.assertIsInstance(result, dict)
            self.assertTrue(name in result.get('message'))
        client._channel.close()

    def test_not_support_service(self):
        client = StubClient(self.default_endpoint, [_GREETER])
        not_support_service = 'notSupport'
        with self.assertRaises(ValueError) as context:
            client.unary_stream(not_support_service, self.method, {'name': "sinsky"})
        exception_msg = f"{context.exception}"
        # print(exception_msg)
        self.assertTrue(f"server doesn't support {not_support_service}" in exception_msg)
        for service in ('helloworld.Greeter',):
            self.assertTrue(service in exception_msg)
        client._channel.close()

    def test_not_support_method(self):
        client = StubClient(self.default_endpoint, [_GREETER])
        not_support_method = 'notSupport'
        with self.assertRaises(ValueError) as context:
            client.unary_stream(self.service, not_support_method, {'name': "sinsky"})
        exception_msg = f"{context.exception}"
        # print(exception_msg)
        self.assertTrue(f"{self.service} doesn't support {not_support_method} method" in exception_msg)
        for method in ('HelloEveryone', 'SayHello', 'SayHelloGroup', 'SayHelloOneByOne'):
            self.assertTrue(method in exception_msg)
        client._channel.close()


class StreamStreamTestCase(RealServerTestCase):
    app = app
    service = 'helloworld.Greeter'
    method = 'SayHelloOneByOne'
    reset_descriptor_pool = False

    def test_success_request(self):
        client = StubClient(self.default_endpoint, [_GREETER])
        names = ['sinsky', 'summer', 'wone']
        _results = client.stream_stream(self.service, self.method, ({"name": name} for name in names))

        results = [x for x in _results]
        print(results)
        self.assertEqual(len(names), len(results))

        for result, name in zip(_results, names):
            self.assertIsInstance(result, dict)
            self.assertTrue(name in result.get('message'))
        client._channel.close()

    def test_not_support_service(self):
        client = StubClient(self.default_endpoint, [_GREETER])
        not_support_service = 'notSupport'
        with self.assertRaises(ValueError) as context:
            client.stream_stream(not_support_service, self.method, [{'name': "sinsky"}])
        exception_msg = f"{context.exception}"
        # print(exception_msg)
        self.assertTrue(f"server doesn't support {not_support_service}" in exception_msg)
        for service in ('helloworld.Greeter',):
            self.assertTrue(service in exception_msg)
        client._channel.close()

    def test_not_support_method(self):
        client = StubClient(self.default_endpoint, [_GREETER])
        not_support_method = 'notSupport'
        with self.assertRaises(ValueError) as context:
            client.stream_stream(self.service, not_support_method, [{'name': "sinsky"}])
        exception_msg = f"{context.exception}"
        # print(exception_msg)
        self.assertTrue(f"{self.service} doesn't support {not_support_method} method" in exception_msg)
        for method in ('HelloEveryone', 'SayHello', 'SayHelloGroup', 'SayHelloOneByOne'):
            self.assertTrue(method in exception_msg)

        client._channel.close()


class StreamUnaryTestCase(RealServerTestCase):
    app = app
    service = 'helloworld.Greeter'
    method = 'HelloEveryone'
    reset_descriptor_pool = False

    def test_success_request(self):
        client = StubClient(self.default_endpoint, [_GREETER])
        names = ['sinsky', 'summer', 'wone']
        result = client.stream_unary(self.service, self.method, ({"name": name} for name in names))
        self.assertIsInstance(result, dict)
        self.assertTrue(f"{names}" in result.get('message', ''))
        client._channel.close()

    def test_not_support_service(self):
        client = StubClient(self.default_endpoint, [_GREETER])
        not_support_service = 'notSupport'
        with self.assertRaises(ValueError) as context:
            client.stream_unary(not_support_service, self.method, [{'name': "sinsky"}])
        exception_msg = f"{context.exception}"
        # print(exception_msg)
        self.assertTrue(f"server doesn't support {not_support_service}" in exception_msg)
        for service in ('helloworld.Greeter',):
            self.assertTrue(service in exception_msg)
        client._channel.close()

    def test_not_support_method(self):
        client = StubClient(self.default_endpoint, [_GREETER])
        not_support_method = 'notSupport'
        with self.assertRaises(ValueError) as context:
            client.stream_unary(self.service, not_support_method, [{'name': "sinsky"}])
        exception_msg = f"{context.exception}"
        print(exception_msg)
        self.assertTrue(f"{self.service} doesn't support {not_support_method} method" in exception_msg)
        for method in ('HelloEveryone', 'SayHello', 'SayHelloGroup', 'SayHelloOneByOne'):
            self.assertTrue(method in exception_msg)
        client._channel.close()


if __name__ == '__main__':
    unittest.main()
