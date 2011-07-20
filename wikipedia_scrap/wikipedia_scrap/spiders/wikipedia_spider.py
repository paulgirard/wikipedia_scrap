from scrapy.contrib.spiders import CrawlSpider,Rule
import json
from scrapy import log



from wikipedia_scrap.items import WikipediaRevisionItem
from wikipedia_scrap.extractors import NextPageResultJSONExtractor

import urlparse,urllib

class Wikipedia_scrapSpider(CrawlSpider):
    name = "wikipedia_api"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = [  "http://en.wikipedia.org/w/api.php?action=query&prop=revisions&format=json&titles=Global_warming&rvprop=ids|timestamp|flags|user|size|userid|tags|content|comment&rvlimit=500"
    ]
    
    rules = (
        # Extract new page result url
        Rule(NextPageResultJSONExtractor(),callback="parse_edits_json",follow=True),

    )
    
    def parse_edits_json(self,json_response) :
        response_dict=json.loads(json_response.body)
        revisions=[]
        pages=response_dict["query"]["pages"]
        page=pages[pages.keys()[0]]
        for revision in page["revisions"] :
            rv=WikipediaRevisionItem()
            revision["pageid"]=page["pageid"]
            
            for key in revision.keys():
            	if key!="anon":
	                rv[key]=revision[key]
                
            revisions.append(rv)
        return revisions

        
    def parse_start_url(self, response):
    	return self.parse_edits_json(response)