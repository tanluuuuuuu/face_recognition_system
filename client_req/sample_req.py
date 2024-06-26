from __future__ import print_function
import sys
sys.path.append("/home/uulnat/face_recognizer_system")
import grpc
from protobuf.module.face_sys_pb2_grpc import FaceRecognitionStub
from protobuf.module.face_sys_pb2 import ImagePair
import numpy as np
import base64
import cv2

def draw_on(img, faces):
    dimg = cv2.imread(img)
    for i in range(0, len(faces), 4):
        face = np.array([faces[i], faces[i + 1], faces[i + 2], faces[i + 3]])
        box = face.astype(int)
        color = (0, 0, 255)
        cv2.rectangle(dimg, (box[0], box[1]), (box[2], box[3]), color, 2)
    return dimg

def run():
    with grpc.insecure_channel("172.17.0.1:50051") as channel:
        stub = FaceRecognitionStub(channel)

        faceImage = open('/home/uulnat/face_recognizer_system/notebooks/faceImage.png', 'rb').read()
        img_face_b64 = base64.b64encode(faceImage).decode("utf8")

        crowdImage = open('/home/uulnat/face_recognizer_system/notebooks/crowdImage.jpg', 'rb').read()
        img_crowd_b64 = base64.b64encode(crowdImage).decode("utf8")

        data = ImagePair(personFace=img_face_b64, crowdImage=img_crowd_b64)
        response = stub.GetFacePosition(data)
        list_pos = np.frombuffer(response.listPosition, dtype='float32')
        print(list_pos)
        rimg = draw_on('/home/uulnat/face_recognizer_system/notebooks/crowdImage.jpg', list_pos)
        cv2.imwrite("./the_output.jpg", rimg)

if __name__ == "__main__":
    run()