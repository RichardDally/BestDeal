# coding: utf-8

import re
from source import Source
from toolbox import clean_price
from loguru import logger


class NewEgg(Source):
    def __init__(self):
        super().__init__(source_name=__class__.__name__)

    def _enrich_deals_from_soup(self, soup, deals):
        raise NotImplementedError()


if __name__ == '__main__':
    vendor = NewEgg()
    fetched_deals = vendor.fetch_deals(product="2080", url="https://www.newegg.com/global/uk-en/p/pl?d=rtx%202080&N=8000&PageSize=96&order=PRICE")
    for deal in fetched_deals:
        logger.info(deal)
    logger.info('Fetched deals count [{}]'.format(len(fetched_deals)))
