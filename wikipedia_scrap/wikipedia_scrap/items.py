# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class WikipediaUserItem(Item):
    # define the fields for your item here like:
    # name = Field()
    # Define here the models for your scraped items
    login = Field()
    userid=Field()
    editcount = Field()
    registration= Field()
    
class WikipediaRevisionItem(Item):
    pageid= Field()
    parentid=Field()
    minor=Field()
    user=Field()
    userid=Field()
    revid= Field()
    size= Field()
    timestamp= Field()
    content= Field()
    tags=Field()
    comment=Field()
    