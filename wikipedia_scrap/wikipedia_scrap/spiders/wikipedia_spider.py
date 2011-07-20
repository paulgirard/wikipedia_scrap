from scrapy.contrib.spiders import CrawlSpider,Rule
import json
from scrapy import log



from wikipedia_scrap.items import Article,Revision,Template,Link,User
from wikipedia_scrap.extractors import NextPageResultJSONExtractor

import urlparse,urllib,re

class Wikipedia_scrapSpider(CrawlSpider):
    name = "wikipedia_api"
    allowed_domains = ["wikipedia.org"]
    start_urls = [  "http://en.wikipedia.org/w/api.php?action=query&prop=revisions&format=json&rvprop=ids|timestamp|flags|user|size|userid|tags|comment|content&rvlimit=200&titles=Global_warming",/
    "http://zh.wikipedia.org/w/api.php?action=query&prop=revisions&format=json&rvprop=ids|timestamp|flags|user|size|userid|tags|comment|content&rvlimit=200&titles=%E5%85%A8%E7%90%83%E5%8F%98%E6%9A%96",/
    "http://hi.wikipedia.org/w/api.php?action=query&prop=revisions&format=json&rvprop=ids|timestamp|flags|user|size|userid|tags|comment|content&rvlimit=200&titles=%E0%A4%AD%E0%A5%82%E0%A4%AE%E0%A4%82%E0%A4%A1%E0%A4%B2%E0%A5%80%E0%A4%AF_%E0%A4%8A%E0%A4%B7%E0%A5%8D%E0%A4%AE%E0%A5%80%E0%A4%95%E0%A4%B0%E0%A4%A3",/
    "http://ru.wikipedia.org/w/api.php?action=query&prop=revisions&format=json&rvprop=ids|timestamp|flags|user|size|userid|tags|comment|content&rvlimit=200&titles=%D0%93%D0%BB%D0%BE%D0%B1%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B5_%D0%BF%D0%BE%D1%82%D0%B5%D0%BF%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5",/
    "http://ja.wikipedia.org/w/api.php?action=query&prop=revisions&format=json&rvprop=ids|timestamp|flags|user|size|userid|tags|comment|content&rvlimit=200&titles=%E5%9C%B0%E7%90%83%E6%B8%A9%E6%9A%96%E5%8C%96",/
    "http://de.wikipedia.org/w/api.php?action=query&prop=revisions&format=json&rvprop=ids|timestamp|flags|user|size|userid|tags|comment|content&rvlimit=200&titles=Globale_Erw%C3%A4rmung",/
    "http://ko.wikipedia.org/w/api.php?action=query&prop=revisions&format=json&rvprop=ids|timestamp|flags|user|size|userid|tags|comment|content&rvlimit=200&titles=%EC%A7%80%EA%B5%AC_%EC%98%A8%EB%82%9C%ED%99%94",/
    "http://fa.wikipedia.org/w/api.php?action=query&prop=revisions&format=json&rvprop=ids|timestamp|flags|user|size|userid|tags|comment|content&rvlimit=200&titles=%DA%AF%D8%B1%D9%85%E2%80%8C%D8%B4%D8%AF%D9%86_%D8%B2%D9%85%DB%8C%D9%86",/
    "http://ar.wikipedia.org/w/api.php?action=query&prop=revisions&format=json&rvprop=ids|timestamp|flags|user|size|userid|tags|comment|content&rvlimit=200&titles=%D8%A7%D8%AD%D8%AA%D8%B1%D8%A7%D8%B1_%D8%B9%D8%A7%D9%84%D9%85%D9%8A",/
    "http://af.wikipedia.org/w/api.php?action=query&prop=revisions&format=json&rvprop=ids|timestamp|flags|user|size|userid|tags|comment|content&rvlimit=200&titles=Aardverwarming",/
    "http://es.wikipedia.org/w/api.php?action=query&prop=revisions&format=json&rvprop=ids|timestamp|flags|user|size|userid|tags|comment|content&rvlimit=200&titles=Calentamiento_global",/
    "http://pt.wikipedia.org/w/api.php?action=query&prop=revisions&format=json&rvprop=ids|timestamp|flags|user|size|userid|tags|comment|content&rvlimit=200&titles=Aquecimento_global",/
    "http://id.wikipedia.org/w/api.php?action=query&prop=revisions&format=json&rvprop=ids|timestamp|flags|user|size|userid|tags|comment|content&rvlimit=200&titles=Pemanasan_global",/
    "http://it.wikipedia.org/w/api.php?action=query&prop=revisions&format=json&rvprop=ids|timestamp|flags|user|size|userid|tags|comment|content&rvlimit=200&titles=Riscaldamento_globale",/
    "http://fr.wikipedia.org/w/api.php?action=query&prop=revisions&format=json&rvprop=ids|timestamp|flags|user|size|userid|tags|comment|content&rvlimit=200&titles=R%C3%A9chauffement_climatique",]
    
    
    
    rules = (
        # Extract new page result url
        Rule(NextPageResultJSONExtractor(),callback="parse_edits_json",follow=True),

    )


    
    def parse_edits_json(self,json_response) :
        # JSON decoding
        response_dict=json.loads(json_response.body)
        
        # get the language code 
        url=urlparse.urlparse(json_response.url)
        (language,domain,tld)=url.netloc.split(".")
        
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
            rv["language"]=language
            
            # user item
            usr=User()
            usr["pageid"]=pageid
            usr["language"]=language
            
            for fieldname in ["revid","parentid","size","timestamp","comment","userid"] :
                rv[fieldname]=revision[fieldname]
            rv["content"]=revision["*"]
            rv["tags"]=",".join(revision["tags"])
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
               tmp["language"]=language
               #store templates
               templates.append(tmp)
               
            # abstract / article
            sections=rev_content_cleaned.split("==")
           
            links=[]
            articles=[]
            # we need section index to tag link in Abstract i.e. first section
            for sectionindex,section in enumerate(sections) :
                # links t article are [[text|page]]
                wikilinks=re.findall("\[\[(.*?)\]\]",section)
                for wikilink in wikilinks :
                    
                    
                    linktitle=None
                    if "|" in wikilink : 
                    	linkparts=wikilink.split("|")
                    	if len(linkparts)==2:
                    		linktext,linktitle=linkparts
                    else :
                    	linktext=""
                    	linktitle=wikilink
                    if linktitle != None :
                        link=Link()
                        link["revid"]=revid
                        link["pagetitle"]=linktitle
                        link["text"]=linktext
                        link["language"]=language
                        #link are tagged as abstract=True if they are un the first section (i.e. abstract)
                        link["abstract"]=sectionindex==0
                        links.append(link)
                        art=Article()
                        art["pagetitle"]=linktitle
                        art["pageid"]=0
                        art["language"]=language
                        articles.append(art)
        items+=revisions+users+templates+links+articles
        return items   

        
    def parse_start_url(self, response):
        response_dict=json.loads(response.body)
         # get the language code 
        url=urlparse.urlparse(response.url)
        (language,domain,tld)=url.netloc.split(".")
        # get page
        pages=response_dict["query"]["pages"]
        page=pages[pages.keys()[0]]
        pageid=page["pageid"]
        pagetitle=page["title"]
        art=Article()
        art["pageid"]=pageid
        art["pagetitle"]=pagetitle
        art["language"]=language
        return self.parse_edits_json(response)+[art]
