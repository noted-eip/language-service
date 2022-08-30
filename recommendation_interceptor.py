from grpc_interceptor import ServerInterceptor
from grpc_interceptor.exceptions import GrpcException, Internal
from loguru import logger
from typing import Callable, Any
import grpc
import time


class UnaryInterceptor(ServerInterceptor):
    def intercept(
        self,
        method: Callable,
        request: Any,
        context: grpc.ServicerContext,
        method_name: str,
    ) -> Any:
        try:
            duration = time.time()
            res = method(request, context)
            duration = time.time() - duration
            with logger.contextualize(time=duration, method=method_name):
                logger.info("rpc")
            return res
        except GrpcException as e:
            with logger.contextualize(method=method_name):
                logger.info("failed rpc")
            context.set_code(e.status_code)
            context.set_details(e.details)
            raise
        except Exception as e:
            logger.error(e)
            raise Internal(f"Internal server error occured: {e}")
