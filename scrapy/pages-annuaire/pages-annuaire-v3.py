import scrapy, re

class PagesAnnuaireV3Spider(scrapy.Spider):
    name = 'pagesannuairev3'
    start_urls = []
    scraped_url = 'https://www.pages-annuaire.net/particuliers/ville/'
    custom_settings = {
            'FEED_URI' : '%(cities_list)s.csv',
            'FEED_FORMAT': 'csv'
    }

    def __init__(self, city_file='', **kwargs):
        scraped_url = self.scraped_url
        city_file_handler = open(city_file, 'r')
        cities = city_file_handler.readlines()
        for name in cities:
            self.start_urls.append(  f'{scraped_url}{name}' )
        self.cities_list = city_file.replace('.txt', '')
        super().__init__(**kwargs)

    def merge_data( self, response ):
        yield {
                'url': response.meta['url'],
                'name':response.meta['name'],
                'address':response.meta['address'],
                'locate': response.meta['locate'],
                'phone': response.text
       }
        
    def parseItem( self, response ):
        address = response.css('h2::text').extract()
        nm=response.css('.btn-numero::attr("data")').get()
        nm_url = 'https://www.pages-annuaire.net/ajax/getMERNumber?tag=F_RES_DSK_SEO&encodeData=' + nm
        meta = {
                'url': response.url,
                'name': response.css('h1::text').get(),
                'address': '',
                'locate': ''
        }

        if len( address ) > 0:
            meta['address'] = address[0]

        if len( address ) > 1:
            meta['locate'] = address[1]

        yield scrapy.Request( nm_url, callback = self.merge_data,headers={"X-Requested-With": "XMLHttpRequest"}, meta = meta)

        
    def parse(self, response):
        links = response.css('#abonne-listing li a::attr(href)').extract()
        for link in links:
            yield scrapy.Request('https://www.pages-annuaire.net' + link, self.parseItem)

        if not re.search('\?p=(\d+)$', response.url):
            script = response.css('#footer + script').get()
            pages = re.search( "totalPages: (\d+)", script )
            if pages:
                total = pages.group(1)
                for page in range(2, int( total ) + 1):
                    yield scrapy.Request( response.url + '?p=' + str(page), self.parse)

        if not re.search('/[a-z]$', response.url):
            links = response.css('.listing-letters .btn-group a::attr(href)').extract()[1:]
            for link in links:
                yield scrapy.Request('https://www.pages-annuaire.net' + link, self.parse)

