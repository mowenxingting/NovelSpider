# -*- coding: utf-8 -*-

# Scrapy settings for BHSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'BHSpider'

SPIDER_MODULES = ['BHSpider.spiders']
NEWSPIDER_MODULE = 'BHSpider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'BHSpider (+http://www.yourdomain.com)'
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'BHSpider.middlewares.BhspiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'BHSpider.middlewares.BhspiderDownloaderMiddleware': 543,
    #启用自定义的随即切换的UserAgent
    'BHSpider.middlewares.RandomUserAgentMiddleware':543,
    #系统的UserAgent中间件设为None
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    # 'BHSpider.middlewares.ProxyMiddleare':543
    # 启用请求超时时的代理
    'BHSpider.middlewares.HttpbinProxyMiddleware': 543,
   #设置不参与scrapy的自动重试的动作
   'scrapy.downloadermiddlewares.retry.RetryMiddleware':None
}
RANDOM_UA_TYPE= 'random'

PROXY_ADDRS=['http://116.209.59.191:9999','http://111.177.187.75:9999','http://111.177.191.15:9999','http://112.95.27.74:8118','http://218.95.82.157:9000','http://111.177.177.28:9999','http://116.209.53.170:9999','http://111.177.175.125:9999','http://111.177.176.109:9999','http://59.62.6.100:9000','http://119.145.2.98:44129','http://111.177.161.248:9999','http://36.26.225.210:9999','http://115.151.63.154:9999','http://110.52.235.156:9999']
# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'BHSpider.pipelines.BhspiderPipeline': 300,
#}
ITEM_PIPELINES = {
    # 先去重
    'BHSpider.pipelines.DuplicatesPipeline': 300,
    'BHSpider.pipelines.JsonWriterPipeline': 500,
    'BHSpider.pipelines.BhspiderPipeline': 800,
    # 'BHSpider.pipelines.PicPipeline': 900
}
# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
db_configs={
    'db_host' : '127.0.0.1',
    'db_name': 'awesome' ,        #数据库名字，请修改
    'db_user' : 'root'      ,       #数据库账号，请修改
    'db_password' : 'password'    ,     #数据库密码，请修改
    'db_port' : 3306               #数据库端口，在dbhelper中使用
}

CLOSESPIDER_TIMEOUT = 3600
# CLOSESPIDER_PAGECOUNT = 50
# CLOSESPIDER_ITEMCOUNT =500
# CLOSESPIDER_ERRORCOUNT = 0