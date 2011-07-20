# Scrapy settings for wikipedia_scrap project
#
# Here all settings are duplicated which *might* be relevant for the wikipedia_srap project
# If non-default values are chosen, a comment with the default value is provided
#
# More info about settings here: http://doc.scrapy.org/topics/settings.html
# Default values here: https://github.com/insophia/scrapy/blob/master/scrapy/settings/default_settings.py

BOT_NAME = 'Wikipedia_scrap'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['Wikipedia_scrap.spiders']
NEWSPIDER_MODULE = 'Wikipedia_scrap.spiders'
DEFAULT_ITEM_CLASS = 'Wikipedia_scrap.items.WikipediaRevisionItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

LOG_ENABLED = True                  
LOG_LEVEL = 'DEBUG'                 # options: CRITICAL, ERROR, WARNING, INFO, DEBUG
LOG_FILE = 'scrape.log'             # default = None

CONCURRENT_ITEMS = 100
CONCURRENT_REQUESTS_PER_SPIDER = 8
CONCURRENT_SPIDERS = 8
DEFAULT_RESPONSE_ENCODING = 'utf8' # default = ascii

DEPTH_LIMIT = 0
DEPTH_STATS = True

DOWNLOADER_STATS = True
DOWNLOAD_TIMEOUT = 180
DOWNLOAD_DELAY = 0
RANDOMIZE_DOWNLOAD_DELAY = True

MEMUSAGE_NOTIFY_MAIL = False
MEMUSAGE_REPORT = False
MEMUSAGE_WARNING_MB = 0

REDIRECT_MAX_TIMES = 20

SCHEDULER_ORDER = 'DFO'             # DFO or BFO

STATS_DUMP = True                   # default = False
STATS_ENABLED = True