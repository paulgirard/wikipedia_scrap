import urllib,urlparse,json
from scrapy.utils.url import safe_url_string, urljoin_rfc, canonicalize_url, url_is_from_any_domain
from scrapy.link import Link 
########

######



class NextPageResultJSONExtractor() :
        
#    def __init__(self):
#        self.extract_links=[]
    
    def extract_links(self,json_response) :
            # extract query_continue
            response_dict=json.loads(json_response.body)
            new_query_arg=response_dict["query-continue"][response_dict["query-continue"].keys()[0]]
            #print "old url : "+json_response.url
            url=urlparse.urlparse(json_response.url)
            #print url
            query_dict=urlparse.parse_qs(url.query)
            # weird bug ? 
            for k,v in query_dict.iteritems() :
                query_dict[k]=v[0]
                
            #print query_dict
            query_dict.update(new_query_arg)
            new_query=urllib.urlencode(query_dict)
            #new_query= "&".join( [k+"="+v[0] for k,v in query_dict.iteritems()])
            url=urlparse.urlunsplit([url.scheme,url.netloc,url.path,new_query,url.fragment])
            link=Link(url=url)
            return [link]
    
    def process_links(self, links):
        """ Normalize and filter extracted links
        The subclass should override it if neccessary
        """
        return links

    
    def matches(self, url):
        """This extractor matches with any url, since
        it doesn't contain any patterns"""
        return True
    