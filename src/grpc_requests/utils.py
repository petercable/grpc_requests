from pathlib import Path
from google.protobuf.descriptor import Descriptor, MethodDescriptor

import warnings

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

def describe_request(method_descriptor: MethodDescriptor) -> dict:
    """
    Provide a dictionary that describes the fields of a Method request
    with a string description of their types.
    :param method_descriptor: MethodDescriptor
    :return: dict - a mapping of field names to their types
    """
    warnings.warn("This function is deprecated, and will be removed in a future release. Use describe_descriptor() instead.", DeprecationWarning)
    description = {}
    for field in method_descriptor.input_type.fields:
        description[field.name] = FIELD_TYPES[field.type-1]
    return description

def describe_descriptor(descriptor: Descriptor) -> str:
    """
    Prints a human readable description of a protobuf descriptor.
    :param descriptor: Descriptor - a protobuf descriptor
    :return: str - a human readable description of the descriptor
    """
    description = descriptor.full_name

    if descriptor.enum_types:
        description += "\nEnums:"
        for enum in descriptor.enum_types:
            description += f"\n{enum.name}: {enum.values}"

    if descriptor.fields:
        description += "\nFields:"
        for field in descriptor.fields:
            description += f"\n{field.name}: {FIELD_TYPES[field.type-1]}"

    if descriptor.nested_types:
        description += "\nNested Types:"
        for nested_type in descriptor.nested_types:
            description += f"\n{nested_type.name}"

    if descriptor.oneofs:
        description += "\nOneofs:"
        for oneof in descriptor.oneofs:
            description += f"\n{oneof.name}"

    return description