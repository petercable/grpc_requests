from pathlib import Path
from google.protobuf.descriptor import MethodDescriptor


def load_data(_path):
    with open(Path(_path).expanduser(), 'rb') as f:
        data = f.read()
    return data

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
        return float(0.0)
    elif field_type in [3, 5, 6, 7, 15, 16, 17, 18]:
        return -456
    elif field_type in [4, 13, 14]:
        return 123
    elif field_type == 8:
        return True
    elif field_type == 9:
        return "Sample!"
    elif field_type == 12:
        return b"Sample!"
    else:
        raise ValueError(f"Unsupported field type: {field_type}")