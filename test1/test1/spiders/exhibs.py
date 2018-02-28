import scrapy
import uuid
import urllib
import io
import logging
import unicodedata
from scrapy.crawler import CrawlerProcess
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from HTMLParser import HTMLParser
from scrapy.utils.log import configure_logging
from test1.items import ExhibitorItem

class ExhibSpider(scrapy.Spider):
    name="exhibs"
    rooturl='http://www.eisenwarenmesse.com'

    custom_settings = {
        'CONCURRENT_REQUESTS': '40',
    }

    # logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)

    # formatter = logging.Formatter('%(message)s')
    # file_handler = logging.FileHandler('exhibs.log')
    # file_handler.setFormatter(formatter)
    
    # logger.addHandler(file_handler)
    
     
    h = HTMLParser()

    # start_urls = ['http://www.eisenwarenmesse.com/IEM/Exhibitor-search/index.php?fw_goto=aussteller/blaettern&&start=0&paginatevalues={"stichwort":""}']
    url_pattern = 'http://www.eisenwarenmesse.com/IEM/Exhibitor-search/index.php?fw_goto=aussteller/blaettern&&start=%s&paginatevalues={"stichwort":""}'

    _urls = []
    for i in range(0,20*137,20):
        _urls.append(url_pattern % str(i))

    start_urls = _urls

    def parse(self, response):

        exhib_items_tags=response.xpath('//td[@class ="cspacer ca3"]/table/tr/td[1]/a')

        next_page = response.xpath('//div[@class="pagination xhidden-xs"]/div[@class="notmobile"]/a[last()]/@href').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
        
        for a in exhib_items_tags:
            uUrl = a.xpath('@href').extract_first() 
            uTitle = a.xpath('text()').extract_first() 
            
            nUrl = unicodedata.normalize('NFKD', uUrl).encode('ascii','ignore')
            nUrl = '%s%s' %(self.rooturl, nUrl)

            nTitle = (unicodedata.normalize('NFKD', uTitle).encode('ascii','ignore')).strip()
            
            # href = a.split('"')[1]
            # title = (a.split('>')[1]).split('<')[0]

            # if title is not None and len(title) > 0 :
            #     title = self.h.unescape(title).strip()
            # else:
            #     randomuid = str(uuid.uuid1())
            #     title = "notitle_%s" % randomuid
            
            # href = self.h.unescape(href)
            # href = '%s%s' % (self.rooturl, href)
            # self.logger.info('%s %s', title, href )

            request = scrapy.Request(nUrl, callback=self.parse_exhibitor, errback = self.errback_httpbin)
            request.meta["title"] = nTitle
            yield request
            
    def parse_exhibitor(self, response):
        title = response.meta["title"]
        filename = 'htmlpages/%s.html' % title.replace("/"," ")

        html = response.xpath('//div[@class="maincontent"]').extract_first()

        if len(str(html)) > 4:
            exhibitor = ExhibitorItem()
            exhibitor['title'] = title
            exhibitor['html_detail'] = html
            yield exhibitor
        else:
            request = scrapy.Request(response.url, callback=self.parse_exhibitor, errback = self.errback_httpbin)
            request.meta["title"] = title
            yield request

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url) 


