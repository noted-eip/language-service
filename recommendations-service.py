import os, sys, json
from dotenv import load_dotenv 
from concurrent import futures 

import grpc
import recommendationspb.recommendations_pb2_grpc as pb2_grpc
import recommendationspb.recommendations_pb2 as pb2

import pke
from pke.lang import stopwords 

from loguru import logger

# TODO : Better logs (account service's json + format) + Class doc

class RecommendationsService(pb2_grpc.RecommendationsServiceServicer):

    extractor = pke.unsupervised.YAKE()

    def __init__(self, *args, **kwargs):
        self.lang                =       os.getenv("RECOMMENDATIONS_SERVICE_LANG")                 or 'fr'
        self.number_of_results   = int  (os.getenv("RECOMMENDATIONS_SERVICE_NUMBER_OF_KEYWORDS"))  or 5
        self.n_gram_length       = int  (os.getenv("RECOMMENDATIONS_SERVICE_N_GRAM_LENGTH"))       or 2 # between 1 and 3
        self.co_occurence_window = int  (os.getenv("RECOMMENDATIONS_SERVICE_CO_OCCURENCE_WINDOW")) or 3 
        self.threshold           = float(os.getenv("RECOMMENDATIONS_SERVICE_THRESHOLD"))           or 0.75 

    def __candidate_selection_and_weighting(self):
        logger.debug(f"Candidate selection : n gram length: {self.n_gram_length} ; co occurence window: {self.co_occurence_window}")
        self.extractor.candidate_selection(n=self.n_gram_length)
        self.extractor.candidate_weighting(window=self.co_occurence_window, use_stems=False)

    def ExtractKeywords(self, request, context):
        logger.info("ExtractKeywords request being processed")

        self.extractor.load_document(input=request.content,
                                     language=self.lang,
                                     stoplist=stopwords[self.lang],
                                     normalization=None)
        self.__candidate_selection_and_weighting()

        keywords_verbose = self.extractor.get_n_best(n=self.number_of_results, threshold=self.threshold)

        keywords = [keyword_info[0] for keyword_info in keywords_verbose]

        result = {'keywords': keywords}

        return pb2.ExtractKeywordsReply(**result)

# TODO: utils.py or utils/env.py
def get_required_env_variable(name: str) -> str:
    result = os.getenv(name);
    if result is None:
        raise EnvironmentError(f"Please set the {name} env variable")
    return result

# TODO: server.py or main.py
def serve():
    port = get_required_env_variable("RECOMMENDATIONS_SERVICE_PORT");
    max_workers = os.getenv("RECOMMENDATIONS_SERVICE_MAX_WORKERS") or 8;

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    
    pb2_grpc.add_RecommendationsServiceServicer_to_server(RecommendationsService(), server)

    logger.info(f"Opening server on port {port}")
    
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    server.wait_for_termination()

# TODO: main.py
if __name__ == '__main__':
    load_dotenv()
    serve()
