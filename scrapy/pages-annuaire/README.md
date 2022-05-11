Scrapy data from https://www.pages-annuaire.net/particuliers/ville/
according slug of city in txt file.

Run from CLI


     scrapy runspider pages-annuaire-v3.py -a city_file=cities.txt  --set=USER_AGENT=Mozilla
