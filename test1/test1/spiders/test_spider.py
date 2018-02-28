import scrapy
from scrapy.crawler import CrawlerProcess
from HTMLParser import HTMLParser

class TestSpider(scrapy.Spider):
    name="TestSpider"
    rooturl='http://www.eisenwarenmesse.com'
    h = HTMLParser()

    start_urls = ['http://www.eisenwarenmesse.com/IEM/Exhibitor-search/index.php?fw_goto=aussteller/blaettern&&start=%s&paginatevalues={"stichwort":""}']

    def parse(self, response):
        pageurl = response.url



    # def start_requests(self):
        
    #     for i in range(0,20*136,20):
    #         starturl='%s/IEM/Exhibitor-search/index.php?fw_goto=aussteller/blaettern&&start=%s&paginatevalues={"stichwort":""}' % (self.rooturl, i)
            
    #         yield scrapy.Request(url=starturl, callback=self.parse)

    # def parse(self, response):
        
    #     anchors=response.xpath('//td[re:test(@class, "cspacer ca3")]/table/tr/td[1]/a').extract()
    #     pageurl = response.url
    #     self.log('crawling page:\n%s' % pageurl)

        
    #     for a in anchors:
    #         href = a.split('"')[1]
    #         title = (a.split('>')[1]).split('<')[0]

    #         if title is not None and len(href) > 0 :
    #             title = self.h.unescape(title)
    #             self.log('Title: %s \n URL: %s%s' % (title, self.rooturl ,href) )
    #         else:
    #             randomuid = str(uuid.uuid1())
    #             self.log('Title: no_title_%s \n URL: %s%s' % (randomuid, self.rooturl, href ) )
        
    #     #self.log('crawling page:%s' % page)
    #     #i = 0
    #     #for a in anchors:
    #     #    i += 1
    #     #    href = a.split('\"')[1]
    #     #    text = (a.split('>')[1]).split('<')[0]
    #     #    text = h.unescape(text)
    #     #    if(len(text) > 0):
    #     #        self.log('Text: %s \n URL: %s%s' % (text, rooturl, href) )
    #     #    else:
    #     #        self.log('Text: %s \n URL: %s%s' % (i, rooturl, href) )

# process = CrawlerProcess({
#     'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
# })

# process.crawl(TestSpider)
# process.start()