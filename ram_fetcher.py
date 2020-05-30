from dotenv import load_dotenv
from abstract_fetcher import AbstractFetcher
from topachat import TopAchat
from grosbill import GrosBill
from cybertek import Cybertek
from ldlc import LDLC
from pcw import PCW
from loguru import logger
from typing import Dict, Tuple, Optional, List
from source import Source
from pricedatabase import PriceDatabase


class RamFetcher(AbstractFetcher):
    def __init__(self, database: Optional[PriceDatabase]):
        super().__init__(database)

    def _get_tweeted_product_types(self) -> List[str]:
        """
        Return product types you want to appear in tweets (one for each)
        To tweet about all product types: self.database.find_distinct_product_types()
        """
        return ["RYZEN 5 3600X", "RYZEN 7 3700X", "RYZEN 9 3950X", "CORE I9 9900KF", "CORE I9 9900K"]

    def _get_source_product_urls(self) -> Dict[type(Source), Dict[str, str]]:
        return {
            TopAchat: {
            },
            PCW: {
            },
            GrosBill: {
            },
            Cybertek: {
            },
            LDLC: {
            },
        }

    def _get_brand_and_product_type(self, product_description, brand: str, brands: dict, families: dict) -> Tuple[Optional[str], Optional[str]]:
        family = self.find_exactly_one_element(brands[brand], product_description)
        if not family:
            logger.warning(f"Brand not found in product [{product_description}]")
            return None, None

        sub_product_type = self.find_exactly_one_element(families[family], product_description)
        if not sub_product_type:
            logger.warning(f"Product type not found in product [{product_description}]")
            return None, None

        product_type = f"{family} {sub_product_type}"

        return brand, product_type

    def _extract_product_data(self, product_description: str) -> Tuple[Optional[str], Optional[str]]:
        ram_types = ["DDR3", "DDR4", "DDR5"]
        ram_brands = ["AORUS", "BALLISTIX", "CORSAIR", "CRUCIAL", "G.SKILL", "GIGABYTE",
                      "HYPERX", "KINGSTON", "T-FORCE"]

        ram_type = self.find_exactly_one_element(ram_types, product_description)
        brand = self.find_exactly_one_element(ram_brands, product_description)

        # Use regexp ?
        # https://regex101.com/r/VTcK62/2

        # Identify CPU brand

        if not brand:
            logger.warning(f'Brand not found in product [{product_description}]')
            return None, None

        brand = "AMD"
        brands = {"AMD": ["Ryzen 3", "Ryzen 5", "Ryzen 7", "Ryzen 9"]}
        families = {
            "RYZEN 3": ["3200G"],
            "RYZEN 5": ["1600 AF", "1600X", "2600X", "2600", "1400", "3600X", "3600"],
            "RYZEN 7": ["2700X", "3700X", "3800X"],
            "RYZEN 9": ["3900X", "3950X"],
        }
        return self._get_brand_and_product_type(product_description, brand, brands, families)


if __name__ == '__main__':
    load_dotenv()
    db = PriceDatabase(collection_name="RAM")
    fetcher = RamFetcher(db)
    fetcher.continuous_watch()
