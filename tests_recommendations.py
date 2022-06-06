from recommendations_service import RecommendationsService
from collections import namedtuple

# Test file for now, can't test it on my current work env

TextRequest = namedtuple('TextRequest', 'content')

def extract_keywords_test():
    service = RecommendationsService()
    request = TextRequest(content="")
        
    res = service.ExtractKeywords(request, {})
    print(res)

extract_keywords_test()