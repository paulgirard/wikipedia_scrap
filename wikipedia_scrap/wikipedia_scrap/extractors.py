import urllib,urlparse,json
from scrapy.utils.url import safe_url_string, urljoin_rfc, canonicalize_url, url_is_from_any_domain
from scrapy.link import Link 
from scrapy import log
########

######



class NextPageResultJSONExtractor() :
        
    def __init__(self):
        self.links=[]
    
    def extract_links(self,json_response) :
            # extract query_continue
            try:
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
                self.links.append(link)
                return self.links
            except:
                # no more pages to crawl 
                return []            
    
# class OutLinkedArticleExtractor() :
#             
#     def extract_links(self,json_response) :
#             # extract and annotate article if present in Abstract
#             try:
#             
#                 #clean 
#                 del \n
#                 before "{{Featured article}}"
#                 
#             
#                 # abstract 
#                 extract .*==
#                 
#                 # links t article are [[text|page]]
#                 
#                 # template
#                 "{{.*}}"
#                 
#                 Article title, order, abstract
#                 
#             
#                 response_dict=json.loads(json_response.body)
#                 new_query_arg=response_dict["query-continue"][response_dict["query-continue"].keys()[0]]
#                 #print "old url : "+json_response.url
#                 url=urlparse.urlparse(json_response.url)
#                 #print url
#                 query_dict=urlparse.parse_qs(url.query)
#                 # weird bug ? 
#                 for k,v in query_dict.iteritems() :
#                     query_dict[k]=v[0]
#                     
#                 #print query_dict
#                 query_dict.update(new_query_arg)
#                 new_query=urllib.urlencode(query_dict)
#                 #new_query= "&".join( [k+"="+v[0] for k,v in query_dict.iteritems()])
#                 url=urlparse.urlunsplit([url.scheme,url.netloc,url.path,new_query,url.fragment])
#                 link=Link(url=url)
#                 log.msg("end of extract links",log.DEBUG)
#                 self.links.append(link)
#                 return self.links
#             except:
#                 # no more pages to crawl 
#                 return []     