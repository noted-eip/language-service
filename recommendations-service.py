from concurrent import futures # in order to use threads
from dotenv import load_dotenv # dotenv

# grpc and recommendations messages
import grpc
import recommendationspb.recommendations_pb2_grpc as pb2_grpc
import recommendationspb.recommendations_pb2 as pb2

# Keyphrase extraction framework
import pke
from pke.lang import stopwords 

import os # getenv


"""

"""

class RecommendationsService(pb2_grpc.RecommendationsServiceServicer):
    extractor = pke.unsupervised.YAKE()

    lang                = os.getenv("LANG")                or 'fr'
    number_of_results   = os.getenv("NUMBER_OF_KEYWORDS")  or 5
    n_gram_length       = os.getenv("N_GRAM_LENGTH")       or 2 # between 1 and 3
    co_occurence_window = os.getenv("CO_OCCURENCE_WINDOW") or 3 
    threshold           = os.getenv("THRESHOLD")           or 0.75 

    def __init__(self, *args, **kwargs):
        self.extractor.candidate_selection(n=self.n_gram_length)
        self.extractor.candidate_weighting(window=self.co_occurence_window)
        print("Service initialized ✅")

    def ExtractKeywords(self, request, context):
        extractor.load_document(input=request.content,
                                language=self.lang,
                                stoplist=stopwords[lang],
                                normalization=None)

        # Will be represented with a list of tuple as such : [ ("keyword", keyword_score), ... ]
        keywords_verbose = extractor.get_n_best(n=self.number_of_results, threshold=self.threshold)

        keywords = [keyword[0] for keyword in keywords_verbose]

        result = {'keywords': keywords}

        return pb2.ExtractKeywordsReply(**result)

# TODO: utils.py or utils/env.py
def get_env_variable(name: str) -> str:
    result = os.getenv(name);
    if result is None:
        raise EnvironmentError(f"Please set the {name} env variable")
    return result

# TODO: server.py or main.py
def serve():
    port = get_env_variable("PORT");
    max_workers = os.getenv("MAX_WORKERS") or 8;

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    
    pb2_grpc.add_RecommendationsServiceServicer_to_server(RecommendationsService(), server)

    server.add_insecure_port(f'[::]:{port}')
    server.start()
    server.wait_for_termination()

# TODO: main.py
if __name__ == '__main__':
    load_dotenv()
    serve()