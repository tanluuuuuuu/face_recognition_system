from loguru import logger
from utils import open_file_cfg
import grpc
from concurrent import futures
from protobuf.module import face_sys_pb2_grpc
from protobuf.module.face_sys_pb2 import Rectangle

class RouteGuideServicer(face_sys_pb2_grpc.RouteGuideServicer):
    """Provides methods that implement functionality of route guide server."""
    def __init__(self):
        pass

    def GetFacePosition(self, request, context):
        print("GetFacePosition called!")
        print(request)
        return Rectangle(code=0, message="OK", listPosition=b'')

class AIServer:
    def __init__(self, cfg):
        self.server_address = cfg["ai"]["server_address"]
        logger.info("server is starting..")

    def serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        face_sys_pb2_grpc.add_RouteGuideServicer_to_server(RouteGuideServicer(), server)
        server.add_insecure_port(self.server_address)
        server.start()
        logger.info("server started at %s" % (self.server_address))
        try:
            server.wait_for_termination()
        except KeyboardInterrupt:
            pass

        logger.info("server stopped")
