from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ImagePair(_message.Message):
    __slots__ = ("personFace", "crowdImage")
    PERSONFACE_FIELD_NUMBER: _ClassVar[int]
    CROWDIMAGE_FIELD_NUMBER: _ClassVar[int]
    personFace: bytes
    crowdImage: bytes
    def __init__(self, personFace: _Optional[bytes] = ..., crowdImage: _Optional[bytes] = ...) -> None: ...

class Rectangle(_message.Message):
    __slots__ = ("code", "message", "listPosition")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    LISTPOSITION_FIELD_NUMBER: _ClassVar[int]
    code: int
    message: str
    listPosition: bytes
    def __init__(self, code: _Optional[int] = ..., message: _Optional[str] = ..., listPosition: _Optional[bytes] = ...) -> None: ...
