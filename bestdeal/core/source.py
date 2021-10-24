# coding: utf-8

import bs4
import requests
from loguru import logger
from abc import ABCMeta, abstractmethod
from typing import Dict


class Source:
    __metaclass__ = ABCMeta

    def __init__(self, source_name: str) -> None:
        self.source_name = source_name
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 '
                                      '(KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                        'Accept-Encoding': 'none',
                        'Accept-Language': 'en-US,en;q=0.8',
                        'Connection': 'keep-alive'}

    @abstractmethod
    def _enrich_deals_from_soup(self, soup: bs4.BeautifulSoup, deals: Dict[str, str]) -> None:
        """
        HTML parsing is implemented in this method
        """
        pass

    def fetch_deals(self, product, url):
        """
        Beautiful Soup is used to process html.
        Specific parsing is done in _enrich_deals_from_soup method.
        """
        deals = {}
        html = requests.get(url=url, headers=self.headers, timeout=30.0)
        soup = bs4.BeautifulSoup(html.text, 'html.parser')
        current_deal_count = len(deals)
        self._enrich_deals_from_soup(soup, deals)
        fetched_deals_count = len(deals) - current_deal_count
        if not fetched_deals_count:
            logger.warning('Product [{}] has not been found on [{}]'.format(product, self.source_name))
        else:
            logger.info(f'[{fetched_deals_count}] [{product}] from [{self.source_name}] found.')
        return deals
