import os, sys, json

import grpc
import recommendationspb.recommendations_pb2_grpc as pb2_grpc
import recommendationspb.recommendations_pb2 as pb2

import pke
from pke.lang import stopwords 

from loguru import logger

# TODO: Class documentation

class RecommendationsService(pb2_grpc.RecommendationsServiceServicer):

    extractor = pke.unsupervised.YAKE()

    def __init__(self, *args, **kwargs):
        self.lang                =       os.getenv("RECOMMENDATIONS_SERVICE_LANG")                 or 'fr'
        self.number_of_results   = int  (os.getenv("RECOMMENDATIONS_SERVICE_NUMBER_OF_KEYWORDS")   or 5   )  
        self.n_gram_length       = int  (os.getenv("RECOMMENDATIONS_SERVICE_N_GRAM_LENGTH")        or 2   ) # between 1 and 3
        self.co_occurence_window = int  (os.getenv("RECOMMENDATIONS_SERVICE_CO_OCCURENCE_WINDOW")  or 3   )  
        self.threshold           = float(os.getenv("RECOMMENDATIONS_SERVICE_THRESHOLD")            or 0.75)            

    def __candidate_selection_and_weighting(self):
        with logger.contextualize(n_gram_length=self.n_gram_length, co_occurence_window=self.co_occurence_window):
            logger.debug(f"Candidate selection")
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

        return pb2.ExtractKeywordsReply(keywords=keywords)
