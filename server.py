import os
import grpc
import protorepo.noted.recommendations.v1.recommendations_pb2_grpc as recommendationspb_grpc

from utils.env import get_required_env_variable

from concurrent import futures

from recommendations_service import RecommendationsAPI
from recommendation_interceptor import UnaryInterceptor
from loguru import logger


def serve():
    port = get_required_env_variable("RECOMMENDATIONS_SERVICE_PORT")
    max_workers = os.getenv("RECOMMENDATIONS_SERVICE_MAX_WORKERS") or 8

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers), interceptors=[UnaryInterceptor()])

    recommendationspb_grpc.add_RecommendationsAPIServicer_to_server(RecommendationsAPI(), server)

    with logger.contextualize(port=port):
        logger.info("Opening server")

    server.add_insecure_port(f'[::]:{port}')
    server.start()
    server.wait_for_termination()
