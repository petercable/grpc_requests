from pathlib import Path
from google.protobuf.descriptor import MethodDescriptor

# String descriptions of protobuf field types
FIELD_TYPES = [
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

def describe_request(method_descriptor: MethodDescriptor) -> dict[str, str]:
    """
    Provide a dictionary that describes the fields of a Method request
    with a string description of their types.
    :param method_descriptor: MethodDescriptor
    :return: dict - a mapping of field names to their types
    """
    description = {}
    for field in method_descriptor.input_type.fields:
        description[field.name] = FIELD_TYPES[field.type-1]
    return description
