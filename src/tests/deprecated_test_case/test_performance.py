import asyncio
import time

from .app import app
from ..testcase import RealServerAsyncTestCase
from ...grpc_requests import AsyncClient, Client


class PerformanceTestCase(RealServerAsyncTestCase):
    app = app
    service = 'helloworld.Greeter'
    method = 'SayHello'

    async def test_async_request(self):
        client = AsyncClient(self.default_endpoint)
        time_to_sleep = 0.05
        request_count = 50
        max_time = time_to_sleep * request_count

        async def request():
            await client.unary_unary(self.service, self.method, {'name': "sinsky"})
            await asyncio.sleep(time_to_sleep)

        start_time = time.time()

        await asyncio.gather(*(request() for _ in range(request_count)))
        end_time = time.time()

        runtime = end_time - start_time
        print(f"async request {request_count} time and sleep {time_to_sleep} seconds processed time : {runtime}")
        self.assertTrue(runtime < max_time)
        await client._channel.close()

    def test_sync_request(self):
        client = Client(self.default_endpoint)
        time_to_sleep = 0.05
        request_count = 50
        max_time = time_to_sleep * request_count

        def request():
            client.unary_unary(self.service, self.method, {'name': "sinsky"})
            time.sleep(time_to_sleep)

        start_time = time.time()
        for _ in range(request_count):
            request()
        end_time = time.time()

        runtime = end_time - start_time
        print(f"sync request {request_count} time and sleep {time_to_sleep} seconds processed time : {runtime}")
        self.assertTrue(runtime > max_time)
        client._channel.close()
