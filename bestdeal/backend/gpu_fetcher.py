from loguru import logger
from dotenv import load_dotenv
from typing import Dict, Tuple, Optional, List
from bestdeal.backend.abstract_fetcher import AbstractFetcher
from bestdeal.sources.topachat import TopAchat
from bestdeal.sources.grosbill import GrosBill
from bestdeal.sources.pcw import PCW
from bestdeal.sources.rueducommerce import RueDuCommerce
from bestdeal.sources.cybertek import Cybertek
from bestdeal.sources.ldlc import LDLC
from bestdeal.sources.materiel import Materiel
from bestdeal.core.source import Source
from bestdeal.core.pricedatabase import PriceDatabase


class GpuFetcher(AbstractFetcher):
    def __init__(self, database: Optional[PriceDatabase]):
        super().__init__(database)
        self.brands = [
            "GAINWARD",
            "KFA2",
            "GIGABYTE",
            "ZOTAC",
            "MSI",
            "PNY",
            "PALIT",
            "EVGA",
            "ASUS",
            "INNO3D",
            "SAPPHIRE",
            "ASROCK",
        ]

    def _get_tweeted_product_types(self) -> List[str]:
        """
        Return product types you want to appear in tweets (one for each)
        To tweet about all product types: self.database.find_distinct_product_types()
        """
        return ["3070 TI", "3080", "3080 TI", "3090"]

    def _get_source_product_urls(self) -> Dict[type(Source), Dict[str, str]]:
        return {
            PCW: {
                "RADEON": "https://www.pcw.fr/232-amd-radeon",
                "RTX": "https://www.pcw.fr/210-nvidia-geforce-rtx",
            },
            TopAchat: {
                "RTX 3 Stock": "https://www.topachat.com/pages/produits_cat_est_micro_puis_rubrique_est_wgfx_pcie_puis_f_est_58-11733,11575,11447,11884,11445,11883,11446|s-1.html",
                "RADEON": "https://www.topachat.com/pages/produits_cat_est_micro_puis_rubrique_est_wgfx_pcie_puis_f_est_58-8743,10812,10851,8741,10586,10587,8742.html"
            },
            GrosBill: {
                "Nvidia": "https://www.grosbill.com/2-carte_graphique-cat-informatique?tri=P&filtre_page=100&mode=listing&filtre_type_produit=carte_graphique&crits=4289%3a4229%3a4144%3a4533%3a4145%3a4530%3a4146%3a3013",
                "RADEON": "https://www.grosbill.com/3-carte_graphique-ati-type-informatique?page=1&tri=P&filtre_page=100&mode=listing&filtre_type_produit=carte_graphique"
            },
            RueDuCommerce: {
                # TODO: find workaround
                # "2080 TI": "https://www.rueducommerce.fr/rayon/composants-16/carte-graphique-nvidia-1913?sort=prix-croissants&view=list&marchand=rue-du-commerce&it_card_chipset_serie=geforce-rtx-2080-ti"
            },
            Cybertek: {
                "RTX 3 Stock": "https://www.cybertek.fr/carte-graphique-6.aspx?crits=4289%3a4229%3a4144%3a4533%3a4145%3a4530%3a4146",
                "RADEON": "https://www.cybertek.fr/carte-graphique-6.aspx?crits=4053%3a4084%3a3707%3a3990%3a3991%3a3708&order=p%3aa%3b"
            },
            LDLC: {
                "RTX 3 Stock": "https://www.ldlc.com/informatique/pieces-informatique/carte-graphique-interne/c4684/+fdi-1+fv1026-5801+fv121-19183,19184,19185,19365,19509,19800,19801.html",
                "RADEON": "https://www.ldlc.com/informatique/pieces-informatique/carte-graphique-interne/c4684/+fdi-1+fi131-l4h8+foms-1+fv1026-5800+fv121-15666,15667,17714,17715,18248,18293.html?sort=1"
            },
            Materiel:
            {
                # "1660": "https://www.materiel.net/carte-graphique/l426/+fv1026-5801+fv121-17465/",
            }
        }

    def _get_brand_and_product_type(self,
                                    product_description: str,
                                    lineup_type: list,
                                    standard_lineup: list,
                                    higher_lineup: dict) -> Tuple[Optional[str], Optional[str]]:
        brand = self.find_exactly_one_element(self.brands, product_description)
        if not brand:
            logger.warning(f"Brand not found in product [{product_description}]")
            return None, None

        lineup_type_result = self.find_exactly_one_element(lineup_type, product_description)
        product_class = self.find_exactly_one_element(standard_lineup, product_description)

        if lineup_type_result is None:
            # Standard lineup
            product_type = product_class
        elif product_class in higher_lineup[lineup_type_result]:
            # Higher lineup
            product_type = f"{product_class} {lineup_type_result}"
        else:
            # Unknown
            product_type = None

        return brand, product_type

    def _extract_radeon_product_data(self, product_description: str) -> Tuple[Optional[str], Optional[str]]:
        lineup_type = ["XT"]
        standard_lineup = ["5500", "5600", "5700", "550", "570", "580"]  # Order does matter.
        higher_lineup = {"XT": ["5500", "5600", "5700"]}
        return self._get_brand_and_product_type(product_description, lineup_type, standard_lineup, higher_lineup)

    def _extract_nvidia_product_data(self, product_description: str) -> Tuple[Optional[str], Optional[str]]:
        standard_lineup = ["2060", "2070", "2080", "3060", "3070", "3080", "3090"]
        higher_lineup = {
            "TI": ["2080", "3070", "3080"],
            "SUPER": ["2060", "2070", "2080"]
        }
        lineup_type = list(higher_lineup.keys())
        return self._get_brand_and_product_type(product_description, lineup_type, standard_lineup, higher_lineup)

    def _extract_product_data(self, product_description: str) -> Tuple[Optional[str], Optional[str]]:
        # Identify CPU brand
        brand = self.find_exactly_one_element(["RADEON"], product_description)
        if brand == "RADEON":
            return self._extract_radeon_product_data(product_description)

        brand = self.find_exactly_one_element(self.brands, product_description)
        if not brand:
            logger.warning(f"Brand not found in product [{product_description}]")
            return None, None

        return self._extract_nvidia_product_data(product_description)


if __name__ == "__main__":
    load_dotenv()
    db = PriceDatabase(collection_name="GPU")
    fetcher = GpuFetcher(db)
    fetcher.continuous_watch()
