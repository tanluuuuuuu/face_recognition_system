from __future__ import print_function
import sys
sys.path.append("/home/uulnat/face_recognizer_system")
import grpc
from protobuf.module.face_sys_pb2_grpc import RouteGuideStub
from protobuf.module.face_sys_pb2 import ImagePair
import numpy as np

def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = RouteGuideStub(channel)

        faceImage = open('/home/uulnat/face_recognizer_system/notebooks/face1.png','rb')
        faceImageBytes = faceImage.read()

        crowdImage = open('/home/uulnat/face_recognizer_system/notebooks/t1_output.jpg','rb')
        crowdImageBytes = crowdImage.read()

        data = ImagePair(personFace=faceImageBytes, crowdImage=crowdImageBytes)
        response = stub.GetFacePosition(data)
        list_pos = np.frombuffer(response.listPosition, dtype='float32')
        print(list_pos)

if __name__ == "__main__":
    run()