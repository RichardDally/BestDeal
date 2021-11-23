from loguru import logger
from bestdeal.source import Source
from bestdeal.toolbox import clean_price


class PCW(Source):
    def __init__(self):
        super().__init__(source_name=__class__.__name__)

    def _enrich_deals_from_soup(self, soup, deals):
        for product in soup.findAll("div", attrs={"class": "price-and-status d-flex flex-wrap align-items-center"}):
            product_name = product.find("a", attrs={"itemprop": "url"}).text
            product_price = product.find("span", attrs={"class": "price product-price"}).text
            deals[product_name] = clean_price(product_price)


if __name__ == "__main__":
    vendor = PCW()
    fetched_deals = vendor.fetch_deals("AMD", "https://www.pcw.fr/231-amd")
    for deal in fetched_deals:
        logger.info(deal)
    logger.info("Fetched deals count [{}]".format(len(fetched_deals)))
