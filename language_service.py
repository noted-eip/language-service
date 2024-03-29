import os

import protorepo.noted.language.v1.language_pb2_grpc as languagepb_grpc
import protorepo.noted.language.v1.language_pb2 as languagepb

import yake

from summa.summarizer import summarize


LANG_NAMES = {
    'fr': 'french',
    'en': 'english'
}


class LanguageAPI(languagepb_grpc.LanguageAPIServicer):

    def __init__(self, *args, **kwargs):
        self.lang                =       os.getenv("LANGUAGE_SERVICE_LANG")                 or 'fr'
        self.number_of_results   = int  (os.getenv("LANGUAGE_SERVICE_NUMBER_OF_KEYWORDS")   or 5   )
        self.n_gram_length       = int  (os.getenv("LANGUAGE_SERVICE_N_GRAM_LENGTH")        or 2   )
        self.co_occurence_window = int  (os.getenv("LANGUAGE_SERVICE_CO_OCCURENCE_WINDOW")  or 3   )
        self.threshold           = float(os.getenv("LANGUAGE_SERVICE_THRESHOLD")            or 0.75)
        self.extractor = yake.KeywordExtractor(
            lan=self.lang,
            n=self.n_gram_length,
            windowsSize=self.co_occurence_window,
            top=self.number_of_results,
            dedupLim=self.threshold
        )

    def ExtractKeywords(self, request, context):
        keywords_verbose = self.extractor.extract_keywords(request.content)

        keywords = [keyword_info[0] for keyword_info in keywords_verbose]

        return languagepb.ExtractKeywordsResponse(keywords=keywords)

    def ExtractKeywordsBatch(self, request, context):
        response = languagepb.ExtractKeywordsBatchResponse()
        tmp_request = languagepb.ExtractKeywordsRequest()
        for text_to_analyze in request.contents:
            tmp_request.content = text_to_analyze
            response.keywords_array.append(self.ExtractKeywords(tmp_request, context))
        return response

    def Summarize(self, request, context):
        REDUCED_RATIO = float(os.getenv("LANGUAGE_SERVICE_SUMMARIZE_REDUCED_RATIO") or 0.4)
        text_input = request.content
        result = summarize(text_input,
                           words=(REDUCED_RATIO * len(text_input.split())),
                           language=LANG_NAMES[self.lang])
        return languagepb.SummarizeResponse(summary=result)
