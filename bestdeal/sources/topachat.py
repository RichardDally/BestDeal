# coding: utf-8

from bestdeal.core.source import Source
from bestdeal.core.toolbox import clean_price


class TopAchat(Source):
    def __init__(self):
        super().__init__(source_name=__class__.__name__)

    def _enrich_deals_from_soup(self, soup, deals):
        for item in soup.findAll('article', attrs={'class': 'grille-produit'}):
            product_name = item.find('h3').text
            product_price = clean_price(item.find('div', attrs={'itemprop': 'price'}).text)
            deals[product_name] = product_price
