# coding: utf-8

import re
import time
from pricedatabase import PriceDatabase
from abc import ABCMeta, abstractmethod
from source import Source
from typing import Optional, Dict, Tuple, List, Iterable, NamedTuple
from loguru import logger
from toolbox import convert_datetime_to_date
from toolbox import get_north_east_arrow
from toolbox import get_south_east_arrow
from toolbox import get_rightwards_arrow
from toolbox import get_see_no_evil_monkey_emoji
from toolbox import get_today_date, get_today_datetime, get_yesterday_date
from toolbox import get_lizard_emoji
from toolbox import get_money_mouth_face_emoji
from toolbox import get_link_emoji
from toolbox import get_first_place_medal_emoji
from publish import tweet


class AbstractFetcher:
    __metaclass__ = ABCMeta
    Prices = NamedTuple("Prices", [('lowest_ever', float), ('today_lowest', float), ('yesterday_lowest', float)])

    def __init__(self, database: Optional[PriceDatabase]):
        """
        database: PriceDatabase object to access database
        wait_in_seconds: waiting time before two scans
        fetch_prices: scrap data from vendors
        display_lowest: display lowest prices for all product types
        tweet_products: publish on Twitter lowest prices
        """
        self.database = database
        self.wait_in_seconds = 900
        self.fetch_prices = True
        self.display_lowest = True
        self.tweet_products = False

    @abstractmethod
    def _get_source_product_urls(self) -> Dict[type(Source), Dict[str, str]]:
        pass

    @abstractmethod
    def _extract_product_data(self, product_description) -> Tuple[Optional[str], Optional[str]]:
        pass

    @abstractmethod
    def _get_tweeted_product_types(self) -> List[str]:
        pass

    def _retrieve_prices(self, product_type) -> Prices:
        today_lowest = self.database.find_cheapest(product_type, get_today_date())
        yesterday_lowest = self.database.find_cheapest(product_type, get_yesterday_date())
        lowest_ever = self.database.find_cheapest_from_all_times(product_type)

        if today_lowest['product_price'] is None:
            raise Exception(f"Missing today data for product [{product_type}]")

        today_price = float(today_lowest['product_price'])
        yesterday_price = float(yesterday_lowest['product_price']) if yesterday_lowest else None
        lowest_ever_price = float(lowest_ever['product_price']) if lowest_ever else None

        return self.Prices(lowest_ever_price, today_price, yesterday_price)

    def _format_cheapest_product_tweet(self, product_type: str) -> str:
        lowest_ever_price, today_price, yesterday_price = self._retrieve_prices(product_type)
        logger.debug(f"Today price [{today_price}] yesterday price [{yesterday_price}]")

        yesterday_comparison = self._build_comparison("D-1", today_price, yesterday_price)

        if lowest_ever_price and today_price <= lowest_ever_price:
            all_times_comparison = f"All times: {get_first_place_medal_emoji()} lowest price detected !"
        else:
            all_times_comparison = self._build_comparison("All times", today_price, lowest_ever_price)

        # TODO: Improve tweet for CPU !
        tweet_text = \
            f"{today_cheapest['product_name']}\n" \
            f"{get_money_mouth_face_emoji()} {today_cheapest['product_price']}€\n" \
            f"{get_link_emoji()} {today_cheapest['url']}\n" \
            f"{yesterday_comparison}\n" \
            f"From yesterday: {yesterday_cheapest['product_price']}€ \n" \
            f"Lowest spotted: {all_times_cheapest['product_price']}€ ({convert_datetime_to_date(all_times_cheapest['timestamp'])})"
        logger.debug(f"Tweeting [{tweet_text}]")
        return tweet_text

    def _tweet_products(self):
        for product_type in self._get_tweeted_product_types():
            try:
                tweet_text = self._format_cheapest_product_tweet(product_type)
                # tweet(tweet_text)
            except Exception as exception:
                logger.exception(exception)

    @staticmethod
    def _compute_evolution_rate(today_price: Optional[float], reference_price: Optional[float]) -> Optional[float]:
        rate = None
        if today_price and reference_price:
            rate = ((today_price - reference_price) / reference_price) * 100
        else:
            logger.warning(f"Cannot compare today price [{today_price}] with reference price [{reference_price}]")
        return rate

    @staticmethod
    def _stringify_evolution_rate(evolution_rate: Optional[float]) -> str:
        if evolution_rate is None:
            percentage = "Missing data"
        elif evolution_rate > 0.:
            percentage = f"+{round(evolution_rate, 2)}%"
        elif evolution_rate < 0.:
            percentage = f"{round(evolution_rate, 2)}%"
        else:
            percentage = "stable"
        return percentage

    @staticmethod
    def _deduce_trend(evolution_rate: Optional[float]) -> str:
        if evolution_rate is None:
            trend = get_see_no_evil_monkey_emoji()
        elif evolution_rate > 0.:
            trend = get_north_east_arrow()
        elif evolution_rate < 0.:
            trend = get_south_east_arrow()
        else:
            trend = get_rightwards_arrow()
        return trend

    def _build_comparison(self, title, today_price, reference_price):
        evolution_rate = self._compute_evolution_rate(today_price, reference_price)
        percentage = self._stringify_evolution_rate(evolution_rate)
        trend = self._deduce_trend(evolution_rate)
        trend_line = f"{title}: {trend} {percentage}"
        return trend_line

    def main_loop(self):
        try:
            # self.database.delete_price_anomalies()
            if self.fetch_prices:
                self._scrap_and_store()
            if self.display_lowest:
                self._display_best_deals()
            if self.tweet_products:
                self._tweet_products()
        except Exception as exception:
            logger.exception(exception)

    def continuous_watch(self):
        while 1:
            try:
                self.main_loop()
            except KeyboardInterrupt:
                logger.info("Stopping gracefully...")
                break

            try:
                logger.info(f"Waiting [{self.wait_in_seconds}] seconds until next deal watch")
                time.sleep(self.wait_in_seconds)
            except KeyboardInterrupt:
                logger.info("Stopping gracefully...")
                break

    def _scrap_and_store(self):
        """
        Example:
        source_class = TopAchat
        product_url_mapping = {'1660 SUPER': 'https://bit.ly/2CJDkOi'}
        """

        if self.database is None:
            logger.warning("Database is not available.")
            return

        posts = []
        for source_class, product_url_mapping in self._get_source_product_urls().items():
            logger.debug(f"Processing source [{source_class}]")
            source = source_class()

            # Scrap every available products for current source
            for product, url in product_url_mapping.items():
                deals = self._scrap_product(source, product, url)
                if not deals:
                    continue

                # Create posts to insert in mongodb
                for product_name, product_price in deals.items():
                    brand, product_type = self._extract_product_data(product_name)

                    if product_type is None:
                        continue

                    last_price = None
                    last_update = self.database.find_last_price(product_name, get_today_date())
                    if last_update:
                        last_price = last_update["product_price"]
                        if last_price == float(product_price):
                            continue

                    previous_price = f"(previous [{last_price}])" if last_price else ""
                    logger.info(f"New price for [{product_name}] [{product_price}] {previous_price}")

                    post = {"product_name": product_name,
                            "product_brand": brand,
                            "product_type": product_type,
                            "product_price": float(product_price),
                            "source": source.source_name,
                            "url": url,
                            "timestamp": get_today_datetime()}
                    posts.append(post)
                    #logger.debug(post)

        if posts:
            self.database.bulk_insert(posts)
        else:
            logger.info("Nothing to insert")

    def _scrap_product(self, source: Source, product: str, url: str) -> Dict[str, str]:
        """
        Fetch deals for ONE product (one url)
        :return: Dict["product_name"] = "product_price"
        """
        deals = None
        logger.info(f'Fetch [{product}] deals from [{source.source_name}]')
        try:
            deals = source.fetch_deals(product, url)
        except Exception as exception:
            logger.warning('Failed to fetch deals for [{}]. Reason [{}]'.format(source.source_name, exception))
        return deals

    def _display_best_deals(self) -> None:
        if self.database is None:
            logger.warning("Database is not available.")
            return

        today_date = get_today_date()
        logger.info(f"Best deals for [{today_date}]")
        cheapest_products = []
        for product_type in self.database.find_distinct_product_types():
            try:
                cheapest = self.database.find_cheapest(product_type, today_date)
                cheapest_products.append(cheapest)
            except Exception as exception:
                logger.exception(exception)
                continue
        max_lengths = {}
        for product in cheapest_products:
            for key, value in product.items():
                max_lengths.setdefault(key, 0)
                max_lengths[key] = max(max_lengths[key], len(str(value)))
        for product in cheapest_products:
            template = 'Cheapest [{product_type:' + str(max_lengths['product_type']) + '}] ' \
                       '[{product_price:' + str(max_lengths['product_price']) + '}]€' \
                       '[{product_name:' + str(max_lengths['product_name']) + '}] ' \
                       '[{source:' + str(max_lengths['source']) + '}]'
            logger.info(template.format(**product))

    @staticmethod
    def find_exactly_one_element(pattern_data: Iterable, raw_data: str) -> Optional[str]:
        """
        Search a pattern_data among raw_data
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
