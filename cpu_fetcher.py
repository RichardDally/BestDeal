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


class CpuFetcher(AbstractFetcher):
    def __init__(self, database: Optional[PriceDatabase]):
        super().__init__(database)

    def _get_tweeted_product_types(self) -> List[str]:
        """
        Return product types you want to appear in tweets (one for each)
        To tweet about all product types: self.database.find_distinct_product_types()
        """
        return ["RYZEN 5 3600X", "RYZEN 9 3900X"]

    def _get_source_product_urls(self) -> Dict[type(Source), Dict[str, str]]:
        return {
            TopAchat: {
                "INTEL": "https://www.topachat.com/pages/produits_cat_est_micro_puis_rubrique_est_wpr_puis_marque_est_INTEL.html",
                "AMD": "https://www.topachat.com/pages/produits_cat_est_micro_puis_rubrique_est_wpr_puis_ordre_est_P_puis_sens_est_ASC_puis_f_est_3-63|557-8865,8660,8617,10578.html",
            },
            PCW: {
                "INTEL": "https://www.pcw.fr/204-intel?order=product.price.asc",
                "AMD": "https://www.pcw.fr/231-amd",
                "RTX": "https://www.pcw.fr/210-nvidia-geforce-rtx"
            },
            GrosBill: {
                "INTEL": "https://www.grosbill.com/2-processeur_intel-cat-informatique?page=1&tri=w&filtre_page=100&mode=listing&filtre_type_produit=processeur",
                "AMD": "https://www.grosbill.com/2-processeur_amd-cat-informatique?page=1&tri=w&filtre_page=50&mode=listing&filtre_type_produit=processeur#filtre_mini=-1&filtre_maxi=-1&filtre_marque=AMD"
            },
            Cybertek: {
                "Intel Core": "https://www.cybertek.fr/processeur-5/intel-6.aspx",
                "AMD Ryzen": "https://www.cybertek.fr/processeur-5/amd-23.aspx?crits=3789%3a3777%3a3694%3a3987"
            },
            LDLC: {
                "Intel Core": "https://www.ldlc.com/informatique/pieces-informatique/processeur/c4300/+fb-C000000192+fdi-1+foms-1+fv579-3857,5524,5912,6023,6114,7779,15953.html?sort=1",
                "AMD Ryzen": "https://www.ldlc.com/informatique/pieces-informatique/processeur/c4300/+fv579-15490,15637,16016,17684.html?sort=1"
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

    def _extract_intel_product_data(self, product_description) -> Tuple[Optional[str], Optional[str]]:
        brand = "INTEL"
        brands = {"INTEL": ["Core i7", "Core i9"]}
        families = {
            "CORE I7": ["9700K", "10700K"],
            "CORE I9": ["9900KF", "9900K"]  # Order does matter.
        }
        return self._get_brand_and_product_type(product_description, brand, brands, families)

    def _extract_amd_product_data(self, product_description) -> Tuple[Optional[str], Optional[str]]:
        brand = "AMD"
        brands = {"AMD": ["Ryzen 3", "Ryzen 5", "Ryzen 7", "Ryzen 9"]}
        families = {
            "RYZEN 3": ["3200G"],
            "RYZEN 5": ["1600 AF", "1600X", "2600X", "2600", "1400", "3600X", "3600"],
            "RYZEN 7": ["2700X", "3700X", "3800X"],
            "RYZEN 9": ["3900X", "3950X"],
        }
        return self._get_brand_and_product_type(product_description, brand, brands, families)

    def _extract_product_data(self, product_description: str) -> Tuple[Optional[str], Optional[str]]:
        extract_mapping = {
            "AMD":  self._extract_amd_product_data,
            "INTEL": self._extract_intel_product_data
        }
        # Identify CPU brand
        brand = self.find_exactly_one_element(extract_mapping.keys(), product_description)
        if not brand:
            logger.warning(f'Brand not found in product [{product_description}]')
            return None, None

        return extract_mapping[brand](product_description)


if __name__ == '__main__':
    load_dotenv()
    db = PriceDatabase(collection_name="CPU")
    fetcher = CpuFetcher(db)
    fetcher.continuous_watch()
