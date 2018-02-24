import scrapy
from HTMLParser import HTMLParser
import uuid
import urllib
import io
import sys



class ExhibitorSpider(scrapy.Spider):
    name="exhibitors"
    rooturl='http://www.eisenwarenmesse.com'
    h = HTMLParser()
    reload(sys)
    sys.setdefaultencoding('utf8')
    
    def start_requests(self):
        
        for i in range(0,20*2,20):
            starturl='%s/IEM/Exhibitor-search/index.php?fw_goto=aussteller/blaettern&&start=%s&paginatevalues={"stichwort":""}' % (self.rooturl, i)
            
            yield scrapy.Request(url=starturl, callback=self.parse)

    def parse(self, response):
        
        anchors=response.xpath('//td[re:test(@class, "cspacer ca3")]/table/tr/td[1]/a').extract()
        #pageurl = response.url
        #self.log('crawling page:\n%s' % pageurl)

        for a in anchors:
            href = a.split('"')[1]
            title = (a.split('>')[1]).split('<')[0]

            if title is not None and len(title) > 0 :
                title = self.h.unescape(title).strip()
            else:
                randomuid = str(uuid.uuid1())
                title = "notitle_%s" % randomuid
            
            href = self.h.unescape(href)
            href = '%s%s' % (self.rooturl, href)
            #result = urllib.urlopen(href)
            #resulthtml = result.read()
            #filename = '%s.html' % title 
            #with open(filename, 'wb') as f:
            #    f.write(resulthtml)
            #    self.log('Saved file %s' % filename)

            #pdfkit.from_url("%s%s" % (self.rooturl, href), '%s.pdf' % title)

            request = scrapy.Request(href, callback=self.parse_exhibitor)
            request.meta["title"] = title
            yield request

    def parse_exhibitor(self, response):
        title = response.meta["title"]
        filename = 'htmlpages/%s.html' % title.replace("/"," ")

        html = response.xpath('//div[re:test(@class, "platzFuerCross")]').extract_first()
        
        with io.open(filename, 'wb') as f:
            f.write(html)
            self.log('Saved file %s' % filename)
