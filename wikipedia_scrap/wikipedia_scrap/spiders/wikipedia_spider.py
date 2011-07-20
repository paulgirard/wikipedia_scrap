from scrapy.contrib.spiders import CrawlSpider,Rule
import json
from scrapy import log



from wikipedia_scrap.items import Article,Revision,Template,Link,User
from wikipedia_scrap.extractors import NextPageResultJSONExtractor

import urlparse,urllib,re

class Wikipedia_scrapSpider(CrawlSpider):
    name = "wikipedia_api"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = [  "http://en.wikipedia.org/w/api.php?action=query&prop=revisions&format=json&titles=Global_warming&rvprop=ids|timestamp|flags|user|size|userid|tags|comment|content&rvlimit=500"
    ]
    
    rules = (
        # Extract new page result url
        Rule(NextPageResultJSONExtractor(),callback="parse_edits_json",follow=False),

    )


    
    def parse_edits_json(self,json_response) :
        # JSON decoding
        response_dict=json.loads(json_response.body)
        
        items=[]
        # get page
        pages=response_dict["query"]["pages"]
        page=pages[pages.keys()[0]]
        pageid=page["pageid"]
        page_title=page["title"]
        
        revisions=[]
        users=[]
        # iter on revisions
        for revision in page["revisions"] :
            # revision item
            rv=Revision()
            rv["pageid"]=pageid
            
            # user item
            usr=User()
            usr["pageid"]=pageid
            for fieldname in ["revid","parentid","size","timestamp","tags","comment","userid"] :
                rv[fieldname]=revision[fieldname]
            rv["content"]=revision["*"]
            rv["minor"]="minor" in revision.keys()
            for fieldname in ["revid","user","userid"] :
                usr[fieldname]=revision[fieldname]
            revid=rv["revid"]
            #store items
            revisions.append(rv)
            users.append(usr)
                    
            #process content to extract templates and links
            #clean \n
            rev_content_cleaned=re.sub("\n","",rv["content"])
            # template item
            wikitemplates=re.findall("{{.*}}",rev_content_cleaned)
            templates=[]
            for template in templates :
               tmp=Template()
               tmp["template"]=template
               tmp["revid"]=rv["revid"]
               tmp["pageid"]=page["revid"]
               #store templates
               templates.append(tmp)
               
            # abstract / article
            sections=rev_content_cleaned.split("==")
           
            links=[]
            articles=[]
            # we need section index to tag link in Abstract i.e. first section
            for sectionindex,section in enumerate(sections) :
                # links t article are [[text|page]]
                wikilinks=re.findall("[[(.*?)]]",section)
                for wikilink in wikilinks :
                    if "|" in wikilink : 
                    	linktext,linktitle=wikilink.split("|")
                    else :
                    	linktext=""
                    	linktitle=wikilink
                    link=Link()
                    link["revid"]=revid
                    link["pagetitle"]=linktitle
                    link["text"]=linktext
                    #link are tagged as abstract=True if they are un the first section (i.e. abstract)
                    link["abstract"]=sectionindex==0
                    links.append(link)
                    art=Article()
                    art["pagetitle"]=linktitle
                    articles.append(art)
        items+=revisions+users+templates+links+articles
        return items   

        
    def parse_start_url(self, response):
        response_dict=json.loads(response.body)
        # get page
        pages=response_dict["query"]["pages"]
        page=pages[pages.keys()[0]]
        pageid=page["pageid"]
        pagetitle=page["title"]
        art=Article()
        art["pageid"]=pageid
        art["pagetitle"]=pagetitle
        return self.parse_edits_json(response)+[art]