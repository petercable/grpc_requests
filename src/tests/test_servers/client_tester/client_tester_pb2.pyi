from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class TestRequest(_message.Message):
    __slots__ = ["factor", "readings", "uuid", "sample_flag", "request_name", "extra_data"]
    FACTOR_FIELD_NUMBER: _ClassVar[int]
    READINGS_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_FLAG_FIELD_NUMBER: _ClassVar[int]
    REQUEST_NAME_FIELD_NUMBER: _ClassVar[int]
    EXTRA_DATA_FIELD_NUMBER: _ClassVar[int]
    factor: int
    readings: _containers.RepeatedScalarFieldContainer[float]
    uuid: int
    sample_flag: bool
    request_name: str
    extra_data: _containers.RepeatedScalarFieldContainer[bytes]
    def __init__(self, factor: _Optional[int] = ..., readings: _Optional[_Iterable[float]] = ..., uuid: _Optional[int] = ..., sample_flag: bool = ..., request_name: _Optional[str] = ..., extra_data: _Optional[_Iterable[bytes]] = ...) -> None: ...

class TestResponse(_message.Message):
    __slots__ = ["average", "feedback"]
    AVERAGE_FIELD_NUMBER: _ClassVar[int]
    FEEDBACK_FIELD_NUMBER: _ClassVar[int]
    average: float
    feedback: str
    def __init__(self, average: _Optional[float] = ..., feedback: _Optional[str] = ...) -> None: ...
