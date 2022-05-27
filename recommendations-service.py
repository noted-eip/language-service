from concurrent import futures # in order to use threads
from dotenv import load_dotenv # dotenv

# grpc and recommendations messages
import grpc
import recommendationspb.recommendations_pb2_grpc as pb2_grpc
import recommendationspb.recommendations_pb2 as pb2

# Logger
from loguru import logger

# Keyphrase extraction framework
import pke
from pke.lang import stopwords 

import os # getenv


"""
Long term, we will have multiple algorithm to choose from
"""

class RecommendationsService(pb2_grpc.RecommendationsServiceServicer):

    extractor           = pke.unsupervised.YAKE()


    def __init__(self, *args, **kwargs):
        self.lang                =       os.getenv("AI_LANG")                 or 'fr'
        self.number_of_results   = int  (os.getenv("AI_NUMBER_OF_KEYWORDS"))  or 5
        self.n_gram_length       = int  (os.getenv("AI_N_GRAM_LENGTH"))       or 2 # between 1 and 3
        self.co_occurence_window = int  (os.getenv("AI_CO_OCCURENCE_WINDOW")) or 3 
        self.threshold           = float(os.getenv("AI_THRESHOLD"))           or 0.75 

        logger.info("Recommendation service has been successfully initialized")

    def __candidate_selection_and_weighting(self):
        logger.debug("Candidate selection and weighting being processed")
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

        logger.debug(f"Response: {keywords}")
        logger.info("ExtractKeywords response being sent")

        return pb2.ExtractKeywordsReply(**result)

# TODO: utils.py or utils/env.py
def get_required_env_variable(name: str) -> str:
    result = os.getenv(name);
    if result is None:
        raise EnvironmentError(f"Please set the {name} env variable")
    return result

# TODO: server.py or main.py
def serve():
    port = get_required_env_variable("PORT");
    max_workers = os.getenv("MAX_WORKERS") or 8;

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