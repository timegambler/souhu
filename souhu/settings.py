# -*- coding: utf-8 -*-

# Scrapy settings for souhu project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'souhu'

SPIDER_MODULES = ['souhu.spiders']
NEWSPIDER_MODULE = 'souhu.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'souhu (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# 设置最大并发请求
CONCURRENT_REQUESTS = 100

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# 将延迟设置越低越好
DOWNLOAD_DELAY = 0

# 提高日志级别，减少日志打印
# LOG_LEVEL = 'ERROR'

# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 100
CONCURRENT_REQUESTS_PER_IP = 100

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    'souhu.middlewares.SouhuSpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    #    'souhu.middlewares.SouhuDownloaderMiddleware': 543,
    'souhu.middlewares.UserAgentMiddleware': 300
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'souhu.pipelines.SouhuPipeline1': 300,
    'souhu.pipelines.SouhuPipeline2': 301,
    'souhu.pipelines.SouhuPipeline3': 302,
    'souhu.pipelines.DuplicatesPipeline': 303,
    'scrapy_redis.pipelines.RedisPipeline': 100,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html

# 控制下载，因为下载过快会导致服务器虽然响应了，但是数据没有发送过来
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
COMMANDS_MODULE = 'souhu.commands'

# 配置数据库文件
MONGODB_HOST = 'localhost'
# MONGODB_HOST = '149.28.89.97'
MONGODB_PORT = 27017
MONGODB_DBNAME = 'souhu_db'
MONGODB_COLNAME = 'souhu_author_source'
MONGODB_COLNAME2 = 'souhu_page'
MONGODB_COLNAME3 = 'souhu_page_cnt'


# 当系统剩余空间小于FREE_SAPCE时停止爬虫，以G为单位
FREE_SPACE = 2

# 设置每次从数据库中返回的id的数目
SKIP = 1000

# 调用redis,如果没有安装，则注释掉
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER_PERSIST = True
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_ENCODING = 'utf-8'
# REDIS_PARAMS = {‘password’:’123456’}
