# coding: utf-8

import re
from bestdeal.source import Source
from bestdeal.toolbox import clean_price
from loguru import logger


class Cybertek(Source):
    def __init__(self):
        super().__init__(source_name=__class__.__name__)

    @staticmethod
    def remove_garbage_characters(string):
        return string.replace('\r', '').replace('\n', '').replace('\t', '')

    @staticmethod
    def remove_all_span(tag):
        for span_tag in tag.findAll('span'):
            span_tag.replace_with('')

    def _enrich_deals_from_soup(self, soup, deals):
        products = soup.findAll('div', attrs={'class': re.compile('ppp-*')})
        for product in products:
            tag = product.find('div', attrs={'class': re.compile('product*')})
            brand = tag.find('span', attrs={'class': 'marque'}).text
            self.remove_all_span(tag)
            second_part = tag.find('a', attrs={'class': 'prod_txt_left'}).text
            product_name = brand + self.remove_garbage_characters(second_part)
            product_price = clean_price(product.find('div', attrs={'class': 'price_prod_resp'}).text)
            deals[product_name] = product_price


if __name__ == '__main__':
    vendor = Cybertek()
    fetched_deals = vendor.fetch_deals("1660", "https://bit.ly/2uL1bJH")
    for deal in fetched_deals:
        logger.info(deal)
    logger.info('Fetched deals count [{}]'.format(len(fetched_deals)))
