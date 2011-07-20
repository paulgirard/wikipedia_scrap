# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class Revision(Item):
    revid= Field()
    parentid=Field()
    minor=Field()
    size= Field()
    timestamp= Field()
    content= Field()
    tags=Field()
    comment=Field()
    #link to Article
    pageid=Field()
    # link to user
    userid=Field()
    language=Field()

class Article(Item):
    pageid= Field()
    pagetitle=Field()
    language=Field()
    
class Template(Item) :
    template=Field()
    revid=Field()
    pageid=Field()
    language=Field()
 
class Link(Item):
    revid=Field()
    pagetitle=Field()
    text=Field()
    abstract=Field()
    language=Field()
 
class User(Item):
    user=Field()
    userid=Field()
    revid=Field()
    pageid=Field()
    language=Field()