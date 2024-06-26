from __future__ import print_function
import sys
sys.path.append("/home/uulnat/face_recognizer_system")
import grpc
from protobuf.module.face_sys_pb2_grpc import RouteGuideStub
from protobuf.module.face_sys_pb2 import ImagePair

def guide_get_positions(stub):
    data = ImagePair(personFace=b'', crowdImage=b'')
    response = stub.GetFacePosition(data)
    return response

def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = RouteGuideStub(channel)
        response = guide_get_positions(stub)
        print(response)

if __name__ == "__main__":
    run()