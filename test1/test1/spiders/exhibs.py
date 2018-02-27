import scrapy
import uuid
import urllib
import io
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from HTMLParser import HTMLParser

class ExhibSpider(scrapy.Spider):
    name="exhibs"
    rooturl='http://www.eisenwarenmesse.com'
    h = HTMLParser()

    start_urls = ['http://www.eisenwarenmesse.com/IEM/Exhibitor-search/index.php?fw_goto=aussteller/blaettern&&start=0&paginatevalues={"stichwort":""}']


    def parse(self, response):

        exhib_items_tags=response.xpath('//td[@class ="cspacer ca3"]/table/tr/td[1]/a').extract()

        next_page = response.xpath('//div[@class="pagination xhidden-xs"]/div[@class="notmobile"]/a[last()]/@href').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
        
        for a in exhib_items_tags:
            href = a.split('"')[1]
            title = (a.split('>')[1]).split('<')[0]

            if title is not None and len(title) > 0 :
                title = self.h.unescape(title).strip()
            else:
                randomuid = str(uuid.uuid1())
                title = "notitle_%s" % randomuid
            
            href = self.h.unescape(href)
            href = '%s%s' % (self.rooturl, href)

            request = scrapy.Request(href, callback=self.parse_exhibitor, errback = self.errback_httpbin)
            request.meta["title"] = title
            yield request

    def parse_exhibitor(self, response):
        title = response.meta["title"]
        filename = 'htmlpages/%s.html' % title.replace("/"," ")

        html = response.xpath('//div[@class="maincontent"]').extract_first()
        
        if len(str(html)) > 4:
            with io.open(filename, 'wb') as f:
                f.write(str(html))
                self.log('Saved file %s' % filename)
        else:
            filename = '%s.failed'% filename
            self.log('Nothing is captured in %s' % response.url)
            with io.open(filename, 'wb') as f:
                f.write(response.body)

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
