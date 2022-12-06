import os
import grpc
import protorepo.noted.language.v1.language_pb2_grpc as languagepb_grpc

from utils.env import get_required_env_variable

from concurrent import futures

from language_service import LanguageAPI
from language_interceptor import UnaryInterceptor
from loguru import logger


def serve():
    port = get_required_env_variable("LANGUAGE_SERVICE_PORT")
    max_workers = os.getenv("LANGUAGE_SERVICE_MAX_WORKERS") or 8

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers), interceptors=[UnaryInterceptor()])

    languagepb_grpc.add_LanguageAPIServicer_to_server(LanguageAPI(), server)

    with logger.contextualize(port=port):
        logger.info("Opening server")

    server.add_insecure_port(f'[::]:{port}')
    server.start()
    server.wait_for_termination()
