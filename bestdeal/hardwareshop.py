# coding: utf-8

import re
from bestdeal.source import Source
from toolbox import clean_price


class HardwareShop(Source):
    def __init__(self):
        super().__init__(source_name=__class__.__name__)
        raise NotImplementedError()

    def _enrich_deals_from_soup(self, soup, deals):
        items = soup.find_all('li', attrs={'data-ref': re.compile("[A-Za-z0-9]")})
        for item in items:
            product_name = item.find('div', attrs={'class': 'description'}).find('h2').text
            for script_section in soup.findAll('script'):
                if '.price-wrapper' in script_section.text:
                    print(script_section.prettify())
            product_price = clean_price(item.find('div', attrs={'class': 'price_prod_resp'}).text)
            deals[product_name] = product_price
