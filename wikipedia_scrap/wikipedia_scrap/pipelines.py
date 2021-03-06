from scrapy import log
from twisted.enterprise import adbapi
from wikipedia_scrap.items import Article,Revision,Template,Link,User

import time
import MySQLdb.cursors

class MySQLStorePipeline(object):

    def __init__(self):
        # Set WIKIPEDISCRAP_DB_* settings in settings.py
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                db='wikipediaControversies',
                user='controversy_user',
                passwd='controversy_pass',
                cursorclass=MySQLdb.cursors.DictCursor,
                charset='utf8',
                use_unicode=True
            )

    def process_item(self, spider, item):
        # run db query in thread pool
        # log.msg(item,level=log.DEBUG)
#         log.msg(isinstance(item,Article),level=log.DEBUG)
        if isinstance(item,Article) :
             query = self.dbpool.runInteraction(self._insert_article, item)
        elif isinstance(item,Revision) :
             query = self.dbpool.runInteraction(self._insert_revision, item)
        elif isinstance(item, Template) :
             query = self.dbpool.runInteraction(self._insert_template, item)
        elif isinstance(item, Link) :
             query = self.dbpool.runInteraction(self._insert_link, item)
        elif isinstance(item, User) :
             query = self.dbpool.runInteraction(self._insert_user, item)
        query.addErrback(self.handle_error)

        return item

    def _insert_article(self, tx, article):
        # create record if doesn't exist.
        #print article['pagetitle']+" "+str(article['pageid']) 
        tx.execute("insert  IGNORE into article (pagetitle, pageid, language ) values (%s, %s, %s )", (article['pagetitle'], article['pageid'],article['language'],))
        log.msg("Article stored in db: %s" % article['pagetitle'], level=log.DEBUG)
    
    def _insert_revision(self, tx, revision):
        # create record if doesn't exist.
        tx.execute("""insert IGNORE into revision (revid, parentid,minor,size,timestamp,content,comment,tags,pageid,userid,language) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (revision['revid'],revision['parentid'],revision['minor'],revision['size'],revision['timestamp'],revision['content'],revision['comment'],revision['tags'],revision['pageid'],revision['userid'],revision['language'],))
        log.msg("Revision stored in db: %s" % revision['revid'], level=log.DEBUG)

    
    def _insert_user(self, tx, user):
        # create record if doesn't exist.
        tx.execute("insert  IGNORE into user (user,userid,revid,pageid,language) values (%s,%s,%s,%s,%s)", (user['user'],user['userid'],user['revid'],user['pageid'],user['language'],))
        log.msg("User stored in db: %s" % user['user'], level=log.DEBUG)
    
    def _insert_template(self, tx, template):
        # create record if doesn't exist.
        tx.execute("insert IGNORE into template (template,metadata,revid,pageid,language) values (%s,%s,%s,%s,%s)", (template['template'],template['metadata'],template['revid'],template['pageid'],template['language'],))
        log.msg("Template stored in db: %s" % template['template'], level=log.DEBUG)
    
    def _insert_link(self, tx, link):
        # create record if doesn't exist.
        tx.execute("insert IGNORE into link (revid,link,text,abstract,language) values (%s,%s,%s,%s,%s)", (link['revid'],link['link'],link['text'],link['abstract'],link['language'],))
        log.msg("Link stored in db: %s" % link['revid']+"-"+link['link'], level=log.DEBUG)

    def handle_error(self, e):
        log.err(e)

