# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: face_sys.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0e\x66\x61\x63\x65_sys.proto\"3\n\tImagePair\x12\x12\n\npersonFace\x18\x01 \x01(\t\x12\x12\n\ncrowdImage\x18\x02 \x01(\t\"@\n\tRectangle\x12\x0c\n\x04\x63ode\x18\x01 \x01(\x05\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x14\n\x0clistPosition\x18\x03 \x01(\x0c\x32>\n\x0f\x46\x61\x63\x65Recognition\x12+\n\x0fGetFacePosition\x12\n.ImagePair\x1a\n.Rectangle\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'face_sys_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_IMAGEPAIR']._serialized_start=18
  _globals['_IMAGEPAIR']._serialized_end=69
  _globals['_RECTANGLE']._serialized_start=71
  _globals['_RECTANGLE']._serialized_end=135
  _globals['_FACERECOGNITION']._serialized_start=137
  _globals['_FACERECOGNITION']._serialized_end=199
# @@protoc_insertion_point(module_scope)
