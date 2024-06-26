from loguru import logger
from utils import open_file_cfg
import grpc
from concurrent import futures
from protobuf.module import face_sys_pb2_grpc
from protobuf.module.face_sys_pb2 import Rectangle

import numpy as np
from numpy import dot
from numpy.linalg import norm
import cv2
import insightface
from insightface.app import FaceAnalysis
import struct

class RouteGuideServicer(face_sys_pb2_grpc.RouteGuideServicer):
    """Provides methods that implement functionality of route guide server."""
    def __init__(self, det_size, sim_threshold):
        self.det_size = det_size
        self.sim_threshold = sim_threshold
        self.app = self.prepareModel()

    def cosine_similarity(self, a, b):
        cos_sim = dot(a, b)/(norm(a)*norm(b))
        return cos_sim

    def prepareModel(self):
        app = FaceAnalysis(providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
        app.prepare(ctx_id=0, det_size=(self.det_size, self.det_size))
        return app

    def readImage(self, image_byte_string):
        nparr = np.fromstring(image_byte_string , np.uint8)
        img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR) 
        return img_np 
    
    def inferenceSingleImage(self, image_numpy):
        faces = self.app.get(image_numpy)
        return faces

    def GetFacePosition(self, request, context):
        print("GetFacePosition called!")
        
        imageFace = self.readImage(request.personFace)
        imageFaceEmbedding = self.inferenceSingleImage(imageFace)[0].embedding
        
        imageCrowd = self.readImage(request.crowdImage)
        imageCrowdEmbedding = self.inferenceSingleImage(imageCrowd)

        result = []
        for personFace in imageCrowdEmbedding:
            embedding = personFace.embedding
            bbox = personFace.bbox
            score = self.cosine_similarity(imageFaceEmbedding, embedding)
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
        face_sys_pb2_grpc.add_RouteGuideServicer_to_server(RouteGuideServicer(self.det_size, self.sim_threshold), server)
        server.add_insecure_port(self.server_address)
        server.start()
        logger.info("server started at %s" % (self.server_address))
        try:
            server.wait_for_termination()
        except KeyboardInterrupt:
            pass

        logger.info("server stopped")
