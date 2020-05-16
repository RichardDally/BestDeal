# coding: utf-8

from dotenv import load_dotenv
from abstract_fetcher import AbstractFetcher
from topachat import TopAchat
from grosbill import GrosBill
from rueducommerce import RueDuCommerce
from cybertek import Cybertek
from ldlc import LDLC
from mindfactory import MindFactory
from materiel import Materiel
from loguru import logger
from typing import Dict, Tuple, Optional, List
from source import Source
from pricedatabase import PriceDatabase


class NVidiaFetcher(AbstractFetcher):
    def __init__(self, database: Optional[PriceDatabase]):
        super().__init__(database)

    def _get_tweeted_product_types(self) -> List[str]:
        """
        Return product types you want to appear in tweets (one for each)
        To tweet about all product types: self.database.find_distinct_product_types()
        """
        return ["2080", "2080 SUPER", "2080 TI"]

    def _get_source_product_urls(self) -> Dict[type(Source), Dict[str, str]]:
        return {
            TopAchat: {
                '1660 SUPER': 'https://bit.ly/2CJDkOi',
                '1660': 'https://bit.ly/2FLwEld',
                '1660 TI': 'https://bit.ly/2uzOWiG',
                '2060': 'https://bit.ly/2CMzlkr',
                '2070': 'https://bit.ly/2FMNlg0',
                '2080': 'https://bit.ly/2JQck65',
                '2060 Super': 'https://bit.ly/2Y1r2NL',
                '2070 Super': 'https://bit.ly/2YRb8Tj',
                '2080 Super': 'https://bit.ly/2Yp0AJT',
                '2080 TI': 'https://bit.ly/2TG5EXT'
            },
            GrosBill: {
                'Multiple products': 'https://bit.ly/2McijjE'
            },
            RueDuCommerce: {
                # TODO: find workaround
                # "2080 TI": "https://www.rueducommerce.fr/rayon/composants-16/carte-graphique-nvidia-1913?sort=prix-croissants&view=list&marchand=rue-du-commerce&it_card_chipset_serie=geforce-rtx-2080-ti"
            },
            Cybertek: {
                '1060 6GB': 'https://bit.ly/2OyuckC',
                '1660': 'https://bit.ly/2uL1bJH',
                '1660 TI': 'https://bit.ly/2YHhJjx',
                '1660 SUPER': 'https://bit.ly/2OMkPyq',
                '2060': 'https://bit.ly/2OITRYd',
                '2060 SUPER': 'https://bit.ly/2OSyMe2',
                '2070': 'https://bit.ly/2FElIo5',
                '2070 SUPER': 'https://bit.ly/2rzczcX',
                '2080': 'https://bit.ly/2TIQ4uM',
                '2080 SUPER': 'https://bit.ly/2qOGE8y',
                '2080 Ti': 'https://bit.ly/2JSMgaD',
            },
            LDLC: {
                '1660': 'https://www.ldlc.com/informatique/pieces-informatique/carte-graphique-interne/c4684/+foms-1+fv1026-5801+fv121-17465.html',
                '1660 TI': 'https://www.ldlc.com/informatique/pieces-informatique/carte-graphique-interne/c4684/+foms-1+fv1026-5801+fv121-17425.html',
                '1660 SUPER': 'https://www.ldlc.com/informatique/pieces-informatique/carte-graphique-interne/c4684/+foms-1+fv1026-5801+fv121-18053.html',
                '2060': 'https://www.ldlc.com/informatique/pieces-informatique/carte-graphique-interne/c4684/+foms-1+fv1026-5801+fv121-17312.html',
                '2060 SUPER': 'https://www.ldlc.com/informatique/pieces-informatique/carte-graphique-interne/c4684/+foms-1+fv1026-5801+fv121-17729.html',
                '2070': 'https://www.ldlc.com/informatique/pieces-informatique/carte-graphique-interne/c4684/+foms-1+fv1026-5801+fv121-16760.html',
                '2070 SUPER': 'https://www.ldlc.com/informatique/pieces-informatique/carte-graphique-interne/c4684/+foms-1+fv1026-5801+fv121-17730.html',
                '2080': 'https://www.ldlc.com/informatique/pieces-informatique/carte-graphique-interne/c4684/+foms-1+fv1026-5801+fv121-16758.html',
                '2080 SUPER': 'https://www.ldlc.com/informatique/pieces-informatique/carte-graphique-interne/c4684/+foms-1+fv1026-5801+fv121-17731.html',
                '2080 Ti': 'https://www.ldlc.com/informatique/pieces-informatique/carte-graphique-interne/c4684/+foms-1+fv1026-5801+fv121-16759.html',
            },
            MindFactory: {
                '1660': 'https://bit.ly/2QSN019',
                '1660 TI': 'https://bit.ly/2KXXWHk',
                '2060': 'https://bit.ly/2smzDw7',
                '2070': 'https://bit.ly/2DnaWlA',
                '2080': 'https://bit.ly/33kaTRP',
                '2080 TI': 'https://bit.ly/35EpY2h',
            },
            Materiel: {
                # "1660": "https://www.materiel.net/carte-graphique/l426/+fv1026-5801+fv121-17465/",
            }
        }

    def _extract_product_data(self, product_description: str) -> Tuple[Optional[str], Optional[str]]:
        brands = [
            'GAINWARD',
            'KFA2',
            'GIGABYTE',
            'ZOTAC',
            'MSI',
            'PNY',
            'PALIT',
            'EVGA',
            'ASUS',
            'INNO3D',
        ]
        lineup_type = ['TI', 'SUPER']
        standard_lineup = ['1050', '1060', '1660', '1070', '1080', '2060', '2070', '2080', '3070', '3080']
        higher_lineup = {
            'TI': ['1050', '1660', '2080', '3080'],
            'SUPER': ['1660', '2060', '2070', '2080']
        }

        brand = self.find_exactly_one_element(brands, product_description)
        if not brand:
            logger.warning(f'Brand not found in product [{product_description}]')
            return None, None

        lineup_type_result = self.find_exactly_one_element(lineup_type, product_description)
        product_class = self.find_exactly_one_element(standard_lineup, product_description)

        if lineup_type_result is None:
            # Standard lineup
            product_type = product_class
        elif product_class in higher_lineup[lineup_type_result]:
            # Higher lineup
            product_type = f'{product_class} {lineup_type_result}'
        else:
            # Unknown
            product_type = None

        return brand, product_type


if __name__ == '__main__':
    load_dotenv()
    db = PriceDatabase(collection_name='NVidiaGPU')
    fetcher = NVidiaFetcher(db)
    fetcher.continuous_watch()
