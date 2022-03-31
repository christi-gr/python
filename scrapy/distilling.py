#scrapy runspider distilling.py -o distilling-all.csv   --set=USER_AGENT=Mozilla

from scrapy.selector import Selector
import scrapy, re

class DistillingSpider(scrapy.Spider):
    name = 'distilling'
    start_urls = ['https://web.distilling.com/directory/results/results.aspx?AffFilter=Bar+or+Cocktail+Lounge']

    def parseItem( self, response ):
        innerHTML = re.search('document.getElementById\("relatedCategories_canvas"\).innerHTML = \'(.*)\'', response.text)

        related_categories = Selector(text = innerHTML.group(1))
        categories =', '.join(related_categories.css('.RelatedCategories_Category a::text').extract())
        contact_data = response.css('.ListingDetails_Level3_MAINCONTACT::text').extract()
        phone_number = []

        for data in contact_data:
                if data.strip():
                        phone_number.append( data.strip() ) 

        yield {
                'URL': response.url,
                'Company Name':response.css('h2 ::text').get(),
                'Contact Person':response.css('.ListingDetails_Level3_MAINCONTACT a ::text').get(),
                'Contact Phone Number': ','.join( phone_number ),
                'Address 1': response.css('[itemprop="street-address"]::text').get(),
                'City':response.css('[itemprop="locality"]::text').get(),
                'State':response.css('[itemprop="region"]::text').get(),
                'Country': '',
                'Postal Code':response.css('[itemprop="postal-code"]::text').get(),
                'Domain':response.css('.ListingDetails_Level3_VISITSITE a::attr(href)').get(),
                'Category':categories
        }
        
    def parse(self, response):
        links = response.css('.ListingResults_All_CONTAINER .ListingResults_All_ENTRYTITLELEFTBOX a::attr(href)').extract()
        for link in links:
            yield scrapy.Request('https://web.distilling.com' + link, self.parseItem)
