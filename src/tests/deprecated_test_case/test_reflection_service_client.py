from .app import app
from ..testcase import RealServerTestCase
from ...grpc_requests import Client


class ReflectionServiceClientTestCase(RealServerTestCase):
    app = app
    service = 'helloworld.Greeter'

    def test_unary_unary_request(self):
        client = Client(self.default_endpoint)
        svc = client.service(self.service)
        request = {'name': "sinsky"}

        result = svc.SayHello(request)

        self.assertIsInstance(result, dict)
        self.assertEqual(result.get('message'), 'Hello sinsky!')
        client._channel.close()

    def test_unary_stream_request(self):
        client = Client(self.default_endpoint)
        svc = client.service(self.service)
        request = {'name': "sinsky"}

        _results = svc.SayHelloGroup(request)

        results = [x for x in _results]
        self.assertEqual(4, len(results))
        names = ['a', 'b', 'c', 'd']

        for result, name in zip(_results, names):
            self.assertIsInstance(result, dict)
            self.assertTrue(name in result.get('message'))
        client._channel.close()

    def test_stream_stream_request(self):
        client = Client(self.default_endpoint)
        svc = client.service(self.service)

        names = ['sinsky', 'summer', 'wone']
        _results = svc.SayHelloOneByOne(({"name": name} for name in names))

        results = [x for x in _results]
        self.assertEqual(len(names), len(results))

        for result, name in zip(_results, names):
            self.assertIsInstance(result, dict)
            self.assertTrue(name in result.get('message'))
        client._channel.close()

    def test_success_request(self):
        client = Client(self.default_endpoint)
        svc = client.service(self.service)
        names = ['sinsky', 'summer', 'wone']
        result = svc.HelloEveryone(({"name": name} for name in names))
        self.assertIsInstance(result, dict)
        self.assertTrue(f"{names}" in result.get('message', ''))
        client._channel.close()
