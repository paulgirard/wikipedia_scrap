# Scrapy settings for wikipedia_scrap project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'wikipedia_scrap'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['wikipedia_scrap.spiders']
NEWSPIDER_MODULE = 'wikipedia_scrap.spiders'
DEFAULT_ITEM_CLASS = 'wikipedia_scrap.items.WikipediaScrapItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

