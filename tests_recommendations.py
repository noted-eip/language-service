from recommendations_service import RecommendationsAPI
import protorepo.noted.recommendations.v1.recommendations_pb2 as recommendationspb

from collections import namedtuple

from custom_logger import init_logger
from loguru import logger

import os , grpc, grpc_testing, unittest

class TestRecommendationsAPI(unittest.TestCase):
    def __init__(self, methodName):
        super().__init__(methodName)
        init_logger()


    def setUp(self):        
        servicers = {
            recommendationspb.DESCRIPTOR.services_by_name['RecommendationsAPI']: RecommendationsAPI()
        }

        self.test_server = grpc_testing.server_from_dictionary(
            servicers, grpc_testing.strict_real_time())

    def test_extract_keywords_empty_request(self):
        """ expect to get an empty response response 
        """
        content = ""
        request = recommendationspb.ExtractKeywordsRequest(content=content)

        extract_keywords_method = self.test_server.invoke_unary_unary(
            method_descriptor=(recommendationspb.DESCRIPTOR
                                .services_by_name['RecommendationsAPI']
                                .methods_by_name['ExtractKeywords']),
            invocation_metadata={},
            request=request, 
            timeout=None
        )

        response, metadata, code, details = extract_keywords_method.termination()

        self.assertEqual(code, grpc.StatusCode.OK)
        self.assertEqual(hasattr(response, 'keywords'), True)
        self.assertEqual(response.keywords, [])

    def test_extract_keywords_invalid_request_field(self):
        """ expect to get a ValueError 
        """
        self.assertRaises(ValueError, recommendationspb.ExtractKeywordsRequest, invalid_field="")

    def test_extract_keywords_valid_request(self):
        """ expect to get multiple keywords that are in the text 
        """
        number_of_keywords = os.getenv("RECOMMENDATIONS_SERVICE_NUMBER_OF_KEYWORDS") or 5 # TODO: defaults.py

        content = "Les mathématiques se distinguent des autres sciences par un rapport particulier au réel car l'observation et l'expérience ne s'y portent pas sur des objets physiques ; les mathématiques ne sont pas une science empirique. Elles sont de nature entièrement intellectuelle, fondées sur des axiomes déclarés vrais ou sur des postulats provisoirement admis."
        request = recommendationspb.ExtractKeywordsRequest(content=content)

        extract_keywords_method = self.test_server.invoke_unary_unary(
            method_descriptor=(recommendationspb.DESCRIPTOR
                                .services_by_name['RecommendationsAPI']
                                .methods_by_name['ExtractKeywords']),
            invocation_metadata={},
            request=request, 
            timeout=None
        )

        response, metadata, code, details = extract_keywords_method.termination()

        self.assertEqual(code, grpc.StatusCode.OK)
        self.assertEqual(hasattr(response, 'keywords'), True)

        keywords = response.keywords
        self.assertEqual(len(keywords), number_of_keywords)
        for keyword in keywords:
            self.assertTrue(keyword.lower() in content.lower())

    def test_extract_keywords_batch_valid_request(self):
        """ expect to get multiple keywords for each text 
        """
        number_of_keywords = os.getenv("RECOMMENDATIONS_SERVICE_NUMBER_OF_KEYWORDS") or 5 # TODO: defaults.py

        request = recommendationspb.ExtractKeywordsBatchRequest()
        request.contents.append("Historiens ont ignoré Vichy et collaboration. Comité d'histoire de la seconde guerre mondiale créé en 1951 brise le mythe resistancialiste dans les années 1960")
        request.contents.append("Plusieurs facteurs expliquent cette évolution: déclin du parti communiste, mort du général de gaulle en 1970, nouvelles générations n'ont plus ce besoin de glorifier la france")
        request.contents.append("Robert Paxton publie la france de vichy en 1972 montre complicité vichy dans déportation 75 000 juifs")

        extract_keywords_batch_method = self.test_server.invoke_unary_unary(
            method_descriptor=(recommendationspb.DESCRIPTOR
                                .services_by_name['RecommendationsAPI']
                                .methods_by_name['ExtractKeywordsBatch']),
            invocation_metadata={},
            request=request, 
            timeout=None
        )

        response, metadata, code, details = extract_keywords_batch_method.termination()

        self.assertEqual(code, grpc.StatusCode.OK)
        self.assertTrue(hasattr(response, 'keywords_array'))

        keywords_array = response.keywords_array
        self.assertEqual(len(keywords_array), len(request.contents))
        for (keywords_object, content) in zip(keywords_array, request.contents):
            self.assertTrue(hasattr(keywords_object, 'keywords'))
            keywords = keywords_object.keywords
            self.assertEqual(len(keywords), number_of_keywords)
            for single_keyword in keywords:
                self.assertTrue(single_keyword.lower() in content.lower())


if __name__ == '__main__':
    unittest.main()
