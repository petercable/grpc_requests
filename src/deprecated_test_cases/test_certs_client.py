from .app import app
from ..testcase import RealServerTestCase
from ...grpc_requests import Client


class CertificateTestCase(RealServerTestCase):
    app = app
    service = 'helloworld.Greeter'
    method = 'SayHello'
    tls = True

    def test_success_request(self):
        client = Client(self.default_endpoint, ssl=True, credentials=dict(
            root_certificates=self.tls_config['certificate'],
        ))
        result = client.unary_unary(self.service, self.method, {'name': "sinsky"})

        self.assertIsInstance(result, dict)
        self.assertEqual(result.get('message'), 'Hello sinsky!')
        client._channel.close()
