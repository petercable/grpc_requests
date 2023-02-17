from .app import app
from ..testcase import RealServerAsyncTestCase
from ...grpc_requests.aio import AsyncClient


class CertificateAsyncTestCase(RealServerAsyncTestCase):
    app = app
    service = 'helloworld.Greeter'
    method = 'SayHello'
    tls = True

    async def test_success_request(self):
        client = AsyncClient(self.default_endpoint, ssl=True, credentials=dict(
            root_certificates=self.tls_config['certificate'],
        ))
        result = await client.unary_unary(self.service, self.method, {'name': "sinsky"})

        self.assertIsInstance(result, dict)
        self.assertEqual(result.get('message'), 'Hello sinsky!')
        await client._channel.close()
