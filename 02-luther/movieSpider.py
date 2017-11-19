import scrapy


class FestivalSpider(scrapy.Spider):

    name = 'music_festivals'

    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 3,
        "HTTPCACHE_ENABLED": True
    }

    start_urls = [
        'https://www.musicfestivalwizard.com/festival-guide/us-festivals/',
        'https://www.musicfestivalwizard.com/festival-guide/canada-festivals/'
    ]

    def parse(self, response):

        for href in response.xpath(
            '//span[@class="festivaltitle"]/a/@href'
        ).extract():

            yield scrapy.Request(
                url=href,
                callback=self.parse_festival,
                meta={'url': href}
            )

        next_url = response.xpath(
            '//div[@class="pagination"]/ul/li/a[@class="next page-numbers"]\
            /@href'
        ).extract()[0]

        yield scrapy.Request(
            url=next_url,
            callback=self.parse
        )

    def parse_festival(self, response):

        url = response.request.meta['url']

        name = response.xpath('//h1/span/text()').extract()[0]

        location = (
            response.xpath('//div[@id="festival-basics"]/text()').extract()[3])

        dates = (
            response.xpath('//div[@id="festival-basics"]/text()').extract()[5])

        tickets = (
            response.xpath('//div[@id="festival-basics"]/text()').extract()[7])

        website = (
            response.xpath(
                '//div[@id="festival-basics"]/a/@href').extract()[0]
        )

        logo = (
            response.xpath(
                '//div[@id="festival-basics"]/img/@src').extract()[0]
        )

        lineup = (
            response.xpath(
                '//div[@class="lineupguide"]/ul/li/text()').extract() +
            response.xpath(
                '//div[@class="lineupguide"]/ul/li/a/text()').extract()
        )

        yield {
            'url': url,
            'name': name,
            'location': location,
            'dates': dates,
            'tickets': tickets,
            'website': website,
            'logo': logo,
            'lineup': lineup}
