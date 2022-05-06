import scrapy, re

class LocalChSpider(scrapy.Spider):
    name = 'localch'
    scraped_url = 'https://www.local.ch/en/q?page=95&rid=SA08&slot=tel'
    start_urls = []
    base_url = 'https://www.local.ch'

    def __init__(self, what='', where='', **kwargs):
        scraped_url = self.scraped_url
        self.start_urls.append(  f'{scraped_url}&what={what}&where={where}' )
        super().__init__(**kwargs)
    
    def parse( self, response ):
        for card in response.css('.entry-card'):
            phone = card.css('.entry-actions a[title="Call"]::attr("data-overlay-label")').get('')
            phone = re.sub('^\* ', '', phone )
            yield {
                'title': card.css('h2::text').get().strip(),
                'address': card.css('.card-info-address span::text').get('').strip(),
                'phone': phone
            }

        next_url = response.css('.pagination  a[rel="next"]::attr("href")').get()
        if next_url:
            yield scrapy.Request( self.base_url + next_url, self.parse )
