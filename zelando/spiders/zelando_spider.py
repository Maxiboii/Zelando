import scrapy


class ZelandoSpider(scrapy.Spider):
    name = 'zelando'
    allowed_domains = ['zalando.de']

    start_urls = ['https://www.zalando.de/herrenbekleidung/']

    custom_settings = {
        # 'DOWNLOAD_DELAY': 1,
        # 'LOG_LEVEL': 'INFO',
        # 'COOKIES_ENABLED': True,
    }

    def parse(self, response, **kwargs):
        xpath = '//div[@data-zalon-partner-target]//article'
        products = response.xpath(xpath)
        for product in products:
            out = {
                'url': product.xpath('a/@href').get(),
                'name': ''.join(product.xpath('.//header//text()').getall()),
                'image': product.xpath('.//img/@src').get(),
            }
            yield out

        next_page = response.xpath('//nav//a[contains(@href, "?p=")]/@href').getall()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page[-1]),
                                 callback=self.parse)
