from scrapy.contrib.spiders import CrawlSpider,Rule
import json
from scrapy import log



from wikipedia_scrap.items import WikipediaRevisionItem
from wikipedia_scrap.extractors import NextPageResultJSONExtractor

import urlparse,urllib

class Wikipedia_scrapSpider(CrawlSpider):
    name = "wikipedia_api"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = [  "http://en.wikipedia.org/w/api.php?action=query&prop=revisions&format=json&titles=Climate_change&rvprop=ids|timestamp|flags|user|size|userid|tags&rvlimit=5",
    ]
    
    rules = (
        # Extract new page result url
        Rule(NextPageResultJSONExtractor()),

    )
        
        
    def parse_start_url(self, json_response):
        response_dict=json.loads(json_response.body)
        revisions=[]
        pages=response_dict["query"]["pages"]
        page=pages[pages.keys()[0]]
        for revision in page["revisions"] :
            rv=WikipediaRevisionItem()
            revision["pageid"]=page["pageid"]
            
            for key in revision.keys():
                rv[key]=revision[key]
                
            revisions.append(rv)
        return revisions
