import random

from pathlib import Path
from google.protobuf.descriptor import MethodDescriptor

TYPES = [
    'DOUBLE',
    'FLOAT',
    'INT64',
    'UINT64',
    'INT32',
    'FIXED64',
    'FIXED32',
    'BOOL',
    'STRING',
    'GROUP',
    'MESSAGE',
    'BYTES',
    'UINT32',
    'ENUM',
    'SFIXED32',
    'SFIXED64',
    'SINT32',
    'SINT64'
]

def load_data(_path):
    with open(Path(_path).expanduser(), 'rb') as f:
        data = f.read()
    return data

def describe_request(method_descriptor: MethodDescriptor) -> dict:
    description = {}
    for field in method_descriptor.input_type.fields:
        description[field.name] = TYPES[field.type-1]
    return description

def example_message(method_descriptor: MethodDescriptor) -> dict:
    message = {}
    for field in method_descriptor.input_type.fields:
        message[field.name] = random_value(field.type)
    return message

def random_value(field_type: int):
#   TYPE_DOUBLE         = 1
#   TYPE_FLOAT          = 2
#   TYPE_INT64          = 3
#   TYPE_UINT64         = 4
#   TYPE_INT32          = 5
#   TYPE_FIXED64        = 6
#   TYPE_FIXED32        = 7
#   TYPE_BOOL           = 8
#   TYPE_STRING         = 9
#   TYPE_GROUP          = 10
#   TYPE_MESSAGE        = 11
#   TYPE_BYTES          = 12
#   TYPE_UINT32         = 13
#   TYPE_ENUM           = 14
#   TYPE_SFIXED32       = 15
#   TYPE_SFIXED64       = 16
#   TYPE_SINT32         = 17
#   TYPE_SINT64         = 18
    if field_type in [1, 2]:
        return random.uniform(1.0, 100.0)
    elif field_type in [3, 5, 6, 7, 15, 16, 17, 18]:
        return random.randint(-100, 100)
    elif field_type in [4, 13, 14]:
        return random.randint(0, 100)
    elif field_type == 8:
        return random.choice([True, False])
    elif field_type == 9:
        return random.choice(['Apple', 'Blueberry', 'Cranberry', 'Durian'])
    elif field_type == 12:
        return random.randbytes(8)
    else:
        raise ValueError(f"Unsupported field type: {field_type}")