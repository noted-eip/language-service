from recommendations_service import RecommendationsService
import recommendationspb.recommendations_pb2 as pb2

from collections import namedtuple

from custom_logger import init_logger
from loguru import logger

import os , grpc, grpc_testing, unittest

class TestRecommendationsService(unittest.TestCase):
    def __init__(self, methodName):
        super().__init__(methodName)
        init_logger()


    def setUp(self):        
        servicers = {
            pb2.DESCRIPTOR.services_by_name['RecommendationsService']: RecommendationsService()
        }

        self.test_server = grpc_testing.server_from_dictionary(
            servicers, grpc_testing.strict_real_time())

    def test_extract_keywords_empty_request(self):
        """ expect to get an empty response response 
        """
        content = ""
        request = pb2.ExtractKeywordsRequest(content=content)

        extract_keywords_method = self.test_server.invoke_unary_unary(
            method_descriptor=(pb2.DESCRIPTOR
                                .services_by_name['RecommendationsService']
                                .methods_by_name['ExtractKeywords']),
            invocation_metadata={},
            request=request, 
            timeout=None)

        response, metadata, code, details = extract_keywords_method.termination()

        self.assertEqual(code, grpc.StatusCode.OK)
        self.assertEqual(hasattr(response, 'keywords'), True)
        self.assertEqual(response.keywords, [])

    def test_extract_keywords_invalid_request_field(self):
        """ expect to get a ValueError 
        """
        self.assertRaises(ValueError, pb2.ExtractKeywordsRequest, invalid_field="")

    def test_extract_keywords_valid_request(self):
        """ expect to get multiple keywords that are in the text 
        """
        number_of_keywords = os.getenv("RECOMMENDATIONS_SERVICE_NUMBER_OF_KEYWORDS") or 5 # TODO: defaults.py

        content = "Les mathématiques se distinguent des autres sciences par un rapport particulier au réel car l'observation et l'expérience ne s'y portent pas sur des objets physiques ; les mathématiques ne sont pas une science empirique. Elles sont de nature entièrement intellectuelle, fondées sur des axiomes déclarés vrais ou sur des postulats provisoirement admis."
        request = pb2.ExtractKeywordsRequest(content=content)

        extract_keywords_method = self.test_server.invoke_unary_unary(
            method_descriptor=(pb2.DESCRIPTOR
                                .services_by_name['RecommendationsService']
                                .methods_by_name['ExtractKeywords']),
            invocation_metadata={},
            request=request, 
            timeout=None)

        response, metadata, code, details = extract_keywords_method.termination()

        self.assertEqual(code, grpc.StatusCode.OK)
        self.assertEqual(hasattr(response, 'keywords'), True)

        keywords = response.keywords
        self.assertEqual(len(keywords), number_of_keywords)
        for keyword in keywords:
            self.assertTrue(keyword in content)



if __name__ == '__main__':
    unittest.main()