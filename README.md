# grpc_requests

[![PyPI](https://img.shields.io/pypi/v/grpc-requests?style=flat-square)](https://pypi.org/project/grpc-requests)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/grpc-requests?style=flat-square)](https://pypi.org/project/grpc-requests)
[![PyPI download month](https://img.shields.io/pypi/dm/grpc-requests?style=flat-square)](https://pypi.org/project/grpc-requests)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
![Views](https://views.whatilearened.today/views/github/wesky93/grpc_requests.svg)

## GRPC for Humans

Leverage [reflection](https://github.com/grpc/grpc/blob/master/doc/server-reflection.md)
to interact with GRPC in a familiar manner for users of the [requests](https://requests.readthedocs.io/en/latest/) library.

```python
from grpc_requests import Client

client = Client.get_by_endpoint("localhost:50051")
assert client.service_names == ["helloworld.Greeter"]

request_data = {"name": "sinsky"} 
result = client.request("helloworld.Greeter", "SayHello", request_data)
print(result) # {"message":"Hello sinsky"}
```

## Features

- Create a client easily when connecting to servers implementing grpc reflection
- Still support creating a client from stubs when reflection isn't available
- All unary and stream methods supported
- TLS and compression connections supported
- AsyncIO API supported

## Install

```shell script
pip install grpc_requests
```

## Usage

Please read over our [examples page](src/examples/examples.md) for a deeper
dive into how to utilize the library.

## Contributing

We welcome community contributions.

When doing so - please target your pull requests to the `develop` branch
and assign the PR to a maintainer for review. We'll take it from there.

## Questions, Comments, Issues?

For questions, please start a conversation on the [discussions page](https://github.com/wesky93/grpc_requests/discussions)!

For feature requests or bugs, please open an [issue](https://github.com/wesky93/grpc_requests/issues) and assign it the appropriate tag.

## Maintainers

- sinsky - [wesky93](https://github.com/wesky93)
- Wayne Manselle - [ViridianForge](https://github.com/ViridianForge)