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
        log.msg(item,level=log.DEBUG)
        log.msg(isinstance(item,Article),level=log.DEBUG)
        if isinstance(item,Article) :
            query = self.dbpool.runInteraction(self._insert_article, item)
        elif isinstance(item,Revision) :
            log.msg("pipeline "+str(item['revid']))
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
        print article['pagetitle']+" "+str(article['pageid']) 
        tx.execute("insert   into article (pagetitle, pageid ) values (%s, %s )", (article['pagetitle'], article['pageid'],))
        log.msg("Article stored in db: %s" % article['pagetitle'], level=log.DEBUG)
    
    def _insert_revision(self, tx, revision):
        # create record if doesn't exist.
        tx.execute("insert   into revision (revid, parentid,minor,size,timestamp,content,tags,comment,pageid,userid) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (revision['revid'],revision['parentid'],revision['minor'],revision['size'],revision['timestamp'],revision['content'],revision['tags'],revision['comment'],revision['pageid'],revision['userid'],))
        log.msg("Revision stored in db: %s" % revision['revid'], level=log.DEBUG)

    
    def _insert_user(self, tx, user):
        # create record if doesn't exist.
        tx.execute("insert  into user (user,userid,revid,pageid) values (%s,%s,%s,%s)", (user['user'],user['userid'],user['revid'],user['pageid'],))
        log.msg("User stored in db: %s" % user['user'], level=log.DEBUG)
    
    def _insert_template(self, tx, template):
        # create record if doesn't exist.
        tx.execute("insert  into template (template,revid,pageid) values (%s,%s,%s)", (user['template'],user['revid'],user['pageid'],))
        log.msg("Template stored in db: %s" % template['template'], level=log.DEBUG)
    
    def _insert_link(self, tx, link):
        # create record if doesn't exist.
        tx.execute("insert  into link (revid,pagetitle,text,abstract) values (%s,%s,%s,%s)", (link['revid'],link['pagetitle'],link['text'],link['abstract'],))
        log.msg("Link stored in db: %s" % link['revid']+"-"+link['pagetitle'], level=log.DEBUG)

    def handle_error(self, e):
        log.err(e)

