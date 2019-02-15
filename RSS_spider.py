import scrapy

class RSS_spider(scrapy.Spider):
    name = 'RSS_spider'
    start_urls = ['https://xmedias2.morgenweb.de/feed/202-alexa-advanced-de-kall.xml']

    def giveUrl():
        print(start_urls[0])

#    def parse(self, response):
#        for title in response.css('.post-header>h2'):
#            yield {'title': title.css('a ::text').get()}


