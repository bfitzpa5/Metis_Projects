import scrapy
import csv


class KickStarterSpider(scrapy.Spider):

    name = 'kickstarter_projects'

    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 3,
        "HTTPCACHE_ENABLED": True
    }

    with open('/home/bf2398/Metis/projects/04-fletcher/urls.csv') as f:
        reader = csv.reader(f)
        urls = list(reader)

    start_urls = [url[0] for url in urls]


    def parse(self, response):
        xpath_description = '//div[@class="full-description js-full-description responsive-media formatted-lists"]//descendant-or-self::text()'
        xpath_risks = '//div[@class="mb3 mb10-sm mb3 js-risks"]//descendant-or-self::text()'

        description = (' '.join(response.xpath(xpath_description).extract())
                                .replace('\xa0','')
                                .replace('\n','')
                       )
        risks = (' '.join(response.xpath(xpath_risks).extract())
                     .replace('\xa0', '')
                     .replace('\n', '')
                 )

        yield{
            'description': description,
            'risks': risks
        }
