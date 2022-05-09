#run from CLI 
#scrapy runspider villes.py -o villes.csv   --set=USER_AGENT=Mozilla
import scrapy
import re

class LinternauteSpider(scrapy.Spider):
    name = 'linternaute'
    start_urls = ['https://www.linternaute.com/ville/classement/villes/population']
    def parse(self, response):
        for item in response.css('.odTable  tbody tr'):
            slug_url = item.css('td')[1].css('a::attr(href)').get()
            slug_search = re.search('ville/([^/]*)/', slug_url)
            p_text = item.css('td')[2].css("::text").get()
            p_search = re.search('(.*) habitan', p_text)
            if p_search:
                population = p_search.group(1).replace('\xa0', '')

            if slug_search:
                slug = slug_search.group(1).replace('\xa0', '')

            yield {
                    'populations':population,
                    'slug': slug,
                    'name': item.css('td')[1].css('a::text').get()
                    }

        next_p = response.css('.ccmcss_paginator--page li.current + li a::attr(href)').get()
        if next_p:
            yield scrapy.Request('https://www.linternaute.com' + next_p, self.parse)
