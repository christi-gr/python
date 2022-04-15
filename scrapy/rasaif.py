# scrapy runspider rasaif.py -o rasaif-all.csv

import scrapy
import json
from scrapy.selector import Selector

class RasaifSpider(scrapy.Spider):
    name = 'rasaif'
    start_urls = ['https://rasaif.com/?cat=85']
    url = 'https://rasaif.com/wp-admin/admin-ajax.php'

    headers = {
        "authority": "rasaif.com",
        "x-requested-with": "XMLHttpRequest",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://rasaif.com",
        "referer": "https://rasaif.com/?cat=85"
    }

    body = 'action=jet_smart_filters&provider=jet-engine%2Fdefault&defaults%5Bpost_status%5D%5B%5D=publish&defaults%5Bpost_type%5D=post&defaults%5Bposts_per_page%5D=12&defaults%5Bpaged%5D=1&defaults%5Bignore_sticky_posts%5D=1&defaults%5Btax_query%5D%5B0%5D%5Btaxonomy%5D=category&defaults%5Btax_query%5D%5B0%5D%5Bfield%5D=term_id&defaults%5Btax_query%5D%5B0%5D%5Bterms%5D%5B%5D=85&defaults%5Btax_query%5D%5B0%5D%5Boperator%5D=IN&defaults%5Border%5D=ASC&defaults%5Borderby%5D=ID&settings%5Blisitng_id%5D=3672&settings%5Bcolumns%5D=1&settings%5Bcolumns_tablet%5D=&settings%5Bcolumns_mobile%5D=&settings%5Bpost_status%5D%5B%5D=publish&settings%5Buse_random_posts_num%5D=&settings%5Bposts_num%5D=12&settings%5Bmax_posts_num%5D=9&settings%5Bnot_found_message%5D=No+data+was+found&settings%5Bis_masonry%5D=&settings%5Bequal_columns_height%5D=&settings%5Buse_load_more%5D=yes&settings%5Bload_more_id%5D=loadmore&settings%5Bload_more_type%5D=click&settings%5Buse_custom_post_types%5D=&settings%5Bhide_widget_if%5D=&settings%5Bcarousel_enabled%5D=&settings%5Bslides_to_scroll%5D=1&settings%5Barrows%5D=true&settings%5Barrow_icon%5D=fa+fa-angle-left&settings%5Bdots%5D=&settings%5Bautoplay%5D=true&settings%5Bautoplay_speed%5D=5000&settings%5Binfinite%5D=true&settings%5Beffect%5D=slide&settings%5Bspeed%5D=500&settings%5Binject_alternative_items%5D=&settings%5Bscroll_slider_enabled%5D=&settings%5Bscroll_slider_on%5D%5B%5D=desktop&settings%5Bscroll_slider_on%5D%5B%5D=tablet&settings%5Bscroll_slider_on%5D%5B%5D=mobile&settings%5Bcustom_query%5D=&props%5Bfound_posts%5D=8202&props%5Bmax_num_pages%5D=684&props%5Bpage%5D='

    def parseItem(self, response):
        js = json.loads( response.text )
        rows = Selector(text=js['content']).css('.jet-listing-grid__item')
        for row in rows:
            description = row.css('.jet-listing-dynamic-field__content p')
            title = row.css('.jet-listing.jet-listing-dynamic-terms span')
            yield {
                    'title_ar':       "\n".join(title[0].css('::text').extract()),
                    'title_en':       "\n".join(title[1].css('::text').extract()),
                    'description_ar': "\n".join(description[0].css('::text').extract()),
                    'description_en': "\n".join(description[1].css('::text').extract()),
                    }


    def parse(self, response):
        script = response.css('#jet-smart-filters-js-extra ::text').get()
        max_num = json.loads(script.strip()[29:-1])['props']['jet-engine']['default']['max_num_pages']
        for page in range(1,5): #max_num + 1 ):
            yield scrapy.Request(
                url=self.url,
                method='POST',
                dont_filter=True,
                headers=self.headers,
                body=self.body + str( page - 1 ) + '&paged=' + str( page ),
                callback = self.parseItem
            )
