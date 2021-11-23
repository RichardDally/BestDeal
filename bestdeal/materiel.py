# coding: utf-8

from bestdeal.source import Source
from loguru import logger


class Materiel(Source):
    def __init__(self):
        super().__init__(source_name=__class__.__name__)
        self.headers["User-Agent"] = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0"

    def _enrich_deals_from_soup(self, soup, deals):
        """
        TODO: implement
        """
        pass


if __name__ == '__main__':
    vendor = Materiel()
    fetched_deals = vendor.fetch_deals("1660", "https://www.materiel.net/carte-graphique/l426/+fv1026-5801+fv121-17465/")
    for deal in fetched_deals:
        logger.info(deal)
    logger.info('Fetched deals count [{}]'.format(len(fetched_deals)))
