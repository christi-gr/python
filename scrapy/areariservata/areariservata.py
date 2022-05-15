# scrapy runspider areariservata.py -o areariservata-all.csv -a in_csv=names.csv

import scrapy
import csv
import re


class AreariservataSpider(scrapy.Spider):
    name = "areariservata"
    url = "https://areariservata.psy.it/cgi-bin/areariservata/albo_nazionale.cgi"
    start_urls = [
        "https://areariservata.psy.it/cgi-bin/areariservata/albo_nazionale.cgi"
    ]

    headers = {
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "sec-ch-ua-mobile": "?0",
        "Upgrade-Insecure-Requests": "1",
        "Origin": "https://areariservata.psy.it",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
        "Accept": "text/html,application/xhtml xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://areariservata.psy.it/cgi-bin/areariservata/albo_nazionale.cgi",
        "Accept-Language": "en-US,en;q=0.9",
    }

    def __init__(self, in_csv="", **kwargs):
        self.in_csv = in_csv
        super().__init__(**kwargs)

    def parseItem(self, response):
        results_html = response.css(".testo::text").get("0")
        count = re.search("(\d+)$", results_html)

        data = {
            "Cognome": response.meta[
                "surname"
            ],  # response.css('.testo_small tr:nth-child(2) td:nth-child(1)::text').get(''),
            "Nome": response.meta[
                "name"
            ],  # response.css('.testo_small tr:nth-child(2) td:nth-child(2)::text').get(''),
            "PEC": response.css(
                ".testo_small tr:nth-child(2) td:nth-child(3)::attr(data-pec)"
            ).get(""),
            "Count": "",
        }

        if count is not None:
            if int(count.group(1)) != 1:
                data["Count"] = count.group(1)
        else:

            data["Count"] = "Not Found"
        yield data

    def parse(self, response):

        with open(self.in_csv, "r") as f_handler:
            reader = csv.reader(f_handler, delimiter=",")

            for i, line in enumerate(reader):

                # ignore header row
                if i == 0:
                    continue

                (name, surname, p_ordine) = line
                body = f'azione=cerca&cognome={surname}&nome={name}&p_ordine={p_ordine}&sigla='

                yield scrapy.Request(
                    url=self.url,
                    method="POST",
                    dont_filter=True,
                    headers=self.headers,
                    body=body,
                    callback=self.parseItem,
                    meta={"name": name, "surname": surname},
                )

