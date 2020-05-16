# coding: utf-8

import os
from pymongo import MongoClient, ASCENDING
from loguru import logger


class PriceDatabase:
    """
    Powered by MongoDB <3
    https://www.mongodb.com
    """

    def __init__(self, collection_name, client=None):
        self.database_name = "PriceHistorization"
        logger.info('Connecting to database [{}]'.format(self.database_name))
        if client is not None:
            self.client = client
        else:
            self.client = MongoClient(os.environ.get("MONGODB_CONNECTION_STRING"))
        self.database = self.client[self.database_name]
        self.collection = self.database[collection_name]

    def bulk_insert(self, posts):
        logger.debug(f"Inserting [{len(posts)}] posts")
        result = self.collection.insert_many(posts)
        logger.debug(result)

    def find_distinct_product_types(self) -> list:
        return self.collection.distinct("product_type")

    def find_last_price(self, product_name: str, datetime_regex: str):
        """
        Example find_last_price("KFA2 GeForce RTX 2080 Ti EX (1-Click OC), 11 Go", get_today_date())
        """
        cursor = self.collection.find({"product_name": product_name, "timestamp": {'$regex': datetime_regex}})
        cursor = cursor.sort("timestamp", ASCENDING)
        for post in cursor.limit(1):
            return post
        # TODO: implement specific exception
        raise Exception("Missing last price")

    def find_cheapest(self, product_type: str, datetime_regex: str):
        """
        Example: find_cheapest("2080 TI", get_today_date())
        """
        first_cursor = self.collection.find({"product_type": product_type, "timestamp": {'$regex': datetime_regex}})
        second_cursor = first_cursor.sort("product_price", ASCENDING)
        for post in second_cursor.limit(1):
            return post
        # TODO: implement specific exception
        raise Exception("Missing cheapest")

    def find_cheapest_from_all_times(self, product_type: str):
        first_cursor = self.collection.find({"product_type": product_type})
        second_cursor = first_cursor.sort("product_price", ASCENDING)
        for post in second_cursor.limit(1):
            return post
        # TODO: implement specific exception
        raise Exception("Missing ever cheapest")

    def delete_price_anomalies(self) -> None:
        """
        Find GPU priced at 1€, scrapper bugs for instance.
        """
        throttle = 50
        anomaly_filter = {"product_price": {"$lt": throttle}}
        cursor = self.collection.delete_many(anomaly_filter)
        logger.info(f"Deleted [{cursor.deleted_count}] under [{throttle}]€")
