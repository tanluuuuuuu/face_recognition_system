from __future__ import print_function
import sys
sys.path.append("/home/uulnat/face_recognizer_system")
import grpc
from protobuf.module.face_sys_pb2_grpc import RouteGuideStub
from protobuf.module.face_sys_pb2 import ImagePair

def guide_get_one_feature(stub, point):
    feature = stub.GetFeature(point)
    if not feature.location:
        print("Server returned incomplete feature")
        return

    if feature.name:
        print("Feature called %s at %s" % (feature.name, feature.location))
    else:
        print("Found no feature at %s" % feature.location)

def guide_get_feature(stub):
    data = ImagePair(personFace=b'', crowdImage=b'')
    response = stub.GetFacePosition(data)
    return response

def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = RouteGuideStub(channel)
        response = guide_get_feature(stub)
        print(response)

if __name__ == "__main__":
    run()