Scraper will take a CSV as input (first name, last name);

then search on this website (https://areariservata.psy.it/cgi-bin/areariservata/albo_nazionale.cgi)

by filling out the input mask and pressing "cerca" [search]; finally write the output table in an output file.

[Specification File](https://github.com/christi-gr/python/blob/main/scrapy/areariservata/Specs.pdf) 

For run from command line use 

    scrapy runspider areariservata.py -o areariservata-all.csv -a in_csv=names.csv

input file is **names.csv**, which contain name, lastname, p_ordine

output file is **areariservata-all.csv**
