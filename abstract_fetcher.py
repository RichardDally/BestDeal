# coding: utf-8

import re
import time
import pricedatabase
from abc import ABCMeta, abstractmethod
from source import Source
from typing import Optional, Dict
from collections import namedtuple
from loguru import logger


class AbstractFetcher:
    __metaclass__ = ABCMeta

    def __init__(self, database_filename):
        self.wait_in_seconds = 900
        self.database_filename = database_filename
        self.db = pricedatabase.PriceDatabase(self.database_filename)

    def continuous_watch(self):
        while True:
            try:
                self._scrap_and_store()
                self._display_best_deals()
            except Exception as exception:
                logger.exception(exception)
            logger.info('Waiting [{}] seconds until next deal watch'.format(self.wait_in_seconds))
            time.sleep(self.wait_in_seconds)

    def _scrap_and_store(self):
        for source_class, product_url_mapping in self.get_source_product_urls().items():
            source = source_class()
            deals = self._scrap(source, product_url_mapping)
            update_price_details = self._store(source, deals)
            if update_price_details:
                self._format_log_update_price_details(update_price_details)

    def _scrap(self, vendor: Source, product_url_mapping) -> Dict[str, str]:
        deals = None
        logger.info('Fetch deals from [{}]'.format(vendor.source_name))
        try:
            deals = vendor.fetch_deals(product_url_mapping)
        except Exception as exception:
            logger.warning('Failed to fetch deals for [{}]. Reason [{}]'.format(vendor.source_name, exception))
        return deals

    def _store(self, source, deals):
        update_price_details = []
        for product_description, product_price in deals.items():
            brand, product_type = self._extract_product_data(product_description)
            if product_type:
                update_price_detail = self._update_price(product_description, product_type, source.source_name,
                                                        float(product_price))
                if update_price_detail is not None:
                    update_price_details.append(update_price_detail)
            else:
                logger.debug(f'Ignoring [{product_description}]')
        return update_price_details

    def _update_price(self, product_name, product_type, source_name, new_price):
        source_id = self.db.insert_if_necessary(table='source',
                                                columns=['source_name'],
                                                values=[source_name])
        product_id = self.db.insert_if_necessary(table='product',
                                                 columns=['product_name', 'product_type'],
                                                 values=[product_name, product_type])
        today_last_price = self.db.get_last_price_for_today(product_id, source_id)
        update_price_details = None
        UpdatePriceDetails = namedtuple('UpdatePriceDetails', 'product_name source_name new_price today_last_price')
        if today_last_price is None or today_last_price != new_price:
            self.db.add_price(product_id, source_id, new_price, self.db.get_today_datetime())
            update_price_details = UpdatePriceDetails(product_name, source_name, str(new_price), str(today_last_price) if today_last_price else None)
        return update_price_details

    def _display_best_deals(self):
        logger.info('Best deals for [{}]'.format(self.db.get_today_date()))
        cheapest_products = []
        for product_type in self.db.get_all_product_types():
            cheapest = self.db.get_cheapest(product_type, self.db.get_today_date())
            if cheapest is not None:
                cheapest_products.append(cheapest)
        max_lengths = {}
        for product in cheapest_products:
            for key, value in product.items():
                max_lengths.setdefault(key, 0)
                max_lengths[key] = max(max_lengths[key], len(str(value)))
        for product in cheapest_products:
            template = 'Cheapest [{product_type:' + str(max_lengths['product_type']) + '}] ' \
                       '[{histo_price:' + str(max_lengths['histo_price']) + '}]€' \
                       '[{product_name:' + str(max_lengths['product_name']) + '}] ' \
                       '[{source_name:' + str(max_lengths['source_name']) + '}]'
            logger.info(template.format(**product))

    @abstractmethod
    def _extract_product_data(self, product_description):
        pass

    @abstractmethod
    def get_source_product_urls(self):
        pass

    @staticmethod
    def find_exactly_one_element(pattern_data, raw_data) -> Optional[str]:
        """
        Search a pattern_data among raw_data
        Examples:

        """
        result = None
        refined_pattern_tokens = []
        at_least_one_space = r'\s{1,}'
        # Build search pattern for " Tixxx" or "2070SUPER " (there must be at least one space)
        # Avoid to gather "xxxxxTIxxxx"
        for pattern_token in pattern_data:
            refined_pattern_tokens.append(f'{at_least_one_space}{pattern_token}')
            refined_pattern_tokens.append(f'{pattern_token}{at_least_one_space}')
        pattern = r"{}".format('|'.join(refined_pattern_tokens))
        parsed = re.findall(pattern, raw_data, re.IGNORECASE)
        parsed = list(set(map(lambda x: x.strip().upper(), parsed)))
        if len(parsed) > 1:
            logger.warning(f'Parsed data is wrong [{parsed}]')
        elif parsed:
            result = parsed[0]
        return result

    @staticmethod
    def _format_log_update_price_details(update_price_details):
        """
        Bloat code to fit to maximum length
        TODO: refactor this
        """
        product_name_max_length = 0
        source_name_max_length = 0
        new_price_max_length = 0
        today_last_price_max_length = 0
        for detail in update_price_details:
            product_name_max_length = max(product_name_max_length, len(detail.product_name))
            source_name_max_length = max(source_name_max_length, len(detail.source_name))
            new_price_max_length = max(new_price_max_length, len(detail.new_price))
            if detail.today_last_price is not None:
                today_last_price_max_length = max(today_last_price_max_length, len(detail.today_last_price))
        template = 'New price for [{:' + str(product_name_max_length) + '}] from [{:' + str(
            source_name_max_length) + '}] : [{:' + str(new_price_max_length) + '}]{}'
        for detail in update_price_details:
            previous_price_info = ''
            if detail.today_last_price is not None:
                previous_price_info = ' Today last price [{:' + str(today_last_price_max_length) + '}]'
                previous_price_info.format(detail.today_last_price)
            logger.info(template.format(detail.product_name, detail.source_name, detail.new_price, previous_price_info))