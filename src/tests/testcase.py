from google.protobuf import symbol_database as _symbol_database, descriptor_pool as _descriptor_pool
from google.protobuf.descriptor_pool import DescriptorPool
from google.protobuf.symbol_database import SymbolDatabase
from homi.test_case import HomiRealServerTestCase

from ..grpc_requests.client import reset_cached_client


class RealServerTestCase(HomiRealServerTestCase):

    @property
    def default_endpoint(self):
        return f"{self.default_server_config['host']}:{self.default_server_config['port']}"

    def reset_grpc_db(self):
        reset_cached_client()
        _descriptor_pool._DEFAULT = DescriptorPool()
        _symbol_database._DEFAULT = SymbolDatabase(pool=_descriptor_pool.Default())

    def setUp(self):
        self.reset_grpc_db()
        super().setUp()

    def tearDown(self):
        self.test_server.stop(1)
