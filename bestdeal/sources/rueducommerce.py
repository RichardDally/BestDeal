# coding: utf-8

from loguru import logger
from bestdeal.core.source import Source
from bestdeal.core.toolbox import clean_price


class RueDuCommerce(Source):
    """
    https://uselesscsp.com/rue-du-commerce.html
    TLDR: it doesn't work
    Blocked by: https://datadome.co/fr/
    """
    def __init__(self):
        super().__init__(source_name=__class__.__name__)

    def _enrich_deals_from_soup(self, soup, deals):
        for item in soup.find_all('article', attrs={'itemtype': 'http://schema.org/Product'}):
            product_name = item.find('div', attrs={'class': 'summary'}).text
            product_price = clean_price(item.find('div', attrs={'class': 'price'}).text)
            deals[product_name] = product_price


if __name__ == '__main__':
    vendor = RueDuCommerce()
    fetched_deals = vendor.fetch_deals("2080 TI", "https://www.rueducommerce.fr/rayon/composants-16/carte-graphique-nvidia-1913?sort=prix-croissants&view=list&marchand=rue-du-commerce&it_card_chipset_serie=geforce-rtx-2080-ti")
    for deal in fetched_deals:
        logger.info(deal)
    logger.info('Fetched deals count [{}]'.format(len(fetched_deals)))
