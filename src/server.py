from loguru import logger
from utils import open_file_cfg
import grpc
from concurrent import futures
from protobuf.module import face_sys_pb2_grpc
from protobuf.module.face_sys_pb2 import Rectangle

import numpy as np
from numpy import dot
from numpy.linalg import norm
import base64                  
from insightface.app import FaceAnalysis
from PIL import Image
import io
import cv2
from scipy.spatial.distance import cosine

class FaceRecognitionServicer(face_sys_pb2_grpc.FaceRecognitionServicer):
    """Provides methods that implement functionality of route guide server."""
    def __init__(self, det_size, sim_threshold):
        self.det_size = det_size
        self.sim_threshold = sim_threshold
        self.app = self.prepareModel()

    def prepareModel(self):
        app = FaceAnalysis(providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
        app.prepare(ctx_id=0, det_size=(self.det_size, self.det_size))
        return app

    def readImage(self, image_byte_string):
        img_bytes = base64.b64decode(image_byte_string.encode('utf-8'))
        img = Image.open(io.BytesIO(img_bytes))
        img_arr = np.asarray(img)     
        img_bgr = cv2.cvtColor(img_arr, cv2.COLOR_RGB2BGR)  
        return img_bgr
    
    def inferenceSingleImage(self, image_numpy):
        faces = self.app.get(image_numpy)
        return faces

    def GetFacePosition(self, request, context):
        print("GetFacePosition called!")
        
        imageFace = self.readImage(request.personFace)
        imageFaceEmbedding = self.inferenceSingleImage(imageFace)
        if (len(imageFaceEmbedding) > 0):
            imageFaceEmbedding = imageFaceEmbedding[0].embedding
        else:
            return Rectangle(code=1, message="No face Detected", listPosition=b'')
        
        imageCrowd = self.readImage(request.crowdImage)
        imageCrowdEmbedding = self.inferenceSingleImage(imageCrowd)

        result = []
        for personFace in imageCrowdEmbedding:
            embedding = personFace.embedding
            bbox = personFace.bbox
            score = 1 - cosine(imageFaceEmbedding, embedding)
            print(score)
            if (score >= self.sim_threshold):
                result.append(bbox)
        result_bytes = np.array(result, dtype='float32').tobytes()

        return Rectangle(code=0, message="OK", listPosition=result_bytes)

class AIServer:
    def __init__(self, cfg):
        self.server_address = cfg["ai"]["server_address"]
        self.det_size = cfg["ai"]["det_size"]
        self.sim_threshold = cfg["ai"]["sim_threshold"]
        logger.info("server is starting..")

    def serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        face_sys_pb2_grpc.add_FaceRecognitionServicer_to_server(FaceRecognitionServicer(self.det_size, self.sim_threshold), server)
        server.add_insecure_port(self.server_address)
        server.start()
        logger.info("server started at %s" % (self.server_address))
        try:
            server.wait_for_termination()
        except KeyboardInterrupt:
            pass

        logger.info("server stopped")
