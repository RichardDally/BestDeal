# coding: utf-8

import bs4
from bestdeal.core.source import Source
from bestdeal.core.toolbox import clean_price


class LDLC(Source):
    def __init__(self):
        super().__init__(source_name=__class__.__name__)

    def _enrich_deals_from_soup(self, soup: bs4.BeautifulSoup, deals):
        for item in soup.find_all("script"):
            if "ecommerce" in item.text:
                for gpu in [x for x in item.text.split("{") if "name" in x]:
                    product_name = None
                    product_price = None
                    # Look for name and price
                    for token in gpu.strip().split(","):
                        if "name" in token:
                            product_name = token.split(":")[1].replace("'", "").strip()
                        elif "price" in token:
                            product_price = token.split(":")[1]
                    if product_name and product_price:
                        deals[product_name] = clean_price(product_price)
                    else:
                        logger.warning(f"Product name [{product_name}] and price [{product_price}] seem not available.")


if __name__ == '__main__':
    from loguru import logger
    vendor = LDLC()
    fetched_deals = vendor.fetch_deals('1660', 'https://bit.ly/2OmH9PP')
    for deal in fetched_deals:
        logger.info(deal)
    logger.info(fetched_deals)
