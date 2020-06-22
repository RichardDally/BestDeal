# coding: utf-8

import os
from pymongo import MongoClient, ASCENDING
from typing import Optional
from loguru import logger
from toolbox import get_today_date


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
        self.tweet_collection = self.database["Tweet"]

    def tweet_exists(self, product_type: str):
        today_date = get_today_date()
        cursor = self.tweet_collection.find({"product_type": product_type, "date": today_date})
        return cursor.count() == 1

    def insert_tweet_status(self, product_type: str):
        today_date = get_today_date()
        post = {"product_type":  product_type,
                "date":          today_date}
        self.tweet_collection.insert(post)

    def bulk_insert(self, posts):
        logger.debug(f"Inserting [{len(posts)}] posts")
        result = self.collection.insert_many(posts)
        logger.debug(result)

    def find_distinct_product_types(self) -> list:
        return self.collection.distinct("product_type")

    def find_last_price(self, product_name: str, datetime_regex: str):
        """
        Example find_last_price("KFA2 GeForce RTX 2080 Ti EX (1-Click OC), 11 Go", get_today_date())
        Do not fetch MindFactory (cannot be ordered from France!)
        """
        cursor = self.collection.find({"product_name": product_name,
                                       "source": {"$ne": "MindFactory"},
                                       "timestamp": {'$regex': datetime_regex}})
        cursor = cursor.sort("timestamp", ASCENDING)
        for post in cursor.limit(1):
            return post
        # TODO: implement specific exception
        raise Exception("Missing last price")

    def find_cheapest(self, product_type: str, timestamp_regex: Optional[str]):
        """
        Example: find_cheapest("2080 TI", get_today_date())
        Do not fetch MindFactory (cannot be ordered from France!)
        """
        post_filter = {"product_type": product_type, "source": {"$ne": "MindFactory"}}
        if timestamp_regex is not None:
            post_filter["timestamp"] = {'$regex': timestamp_regex}
        first_cursor = self.collection.find(post_filter)
        second_cursor = first_cursor.sort("product_price", ASCENDING)
        for post in second_cursor.limit(1):
            return post
        # TODO: implement specific exception
        raise Exception(f"Missing cheapest [{product_type}]")

    def delete_price_anomalies(self) -> None:
        """
        Find GPU priced at 1€, scrapper bugs for instance.
        """
        throttle = 50
        anomaly_filter = {"product_price": {"$lt": throttle}}
        cursor = self.collection.delete_many(anomaly_filter)
        logger.info(f"Deleted [{cursor.deleted_count}] under [{throttle}]€")
