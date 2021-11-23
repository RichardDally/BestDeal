# coding: utf-8

from bestdeal.source import Source
from bestdeal.toolbox import clean_price


class GrosBill(Source):
    def __init__(self):
        super().__init__(source_name=__class__.__name__)

    def _enrich_deals_from_soup(self, soup, deals):
        for product in soup.find('table', attrs={'id': 'listing_mode_display'}).findAll('tr'):
            try:
                product_name = product.find('div', attrs={'class': 'product_description'}).find('a').text
                product_price = clean_price(product.find('td', attrs={'class': 'btn_price_wrapper'}).find('b').text)
                deals[product_name] = product_price
            except Exception as exception:
                pass


# if __name__ == '__main__':
#     vendor = GrosBill()
#     fetched_deals = vendor.fetch_deals()
#     for deal in fetched_deals:
#         logger.info(deal)
#     logger.info('Fetched deals count [{}]'.format(len(fetched_deals)))
