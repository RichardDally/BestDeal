import unittest
from toolbox import get_today_datetime, get_yesterday_datetime
from abstract_fetcher import AbstractFetcher
from pricedatabase import PriceDatabase
from pymongo_inmemory import MongoClient


class TestFetcher(AbstractFetcher):
    def __init__(self, database):
        super().__init__(database)


class TestAbstractFetcher(unittest.TestCase):
    def setUp(self) -> None:
        self.client = MongoClient()
        self.db = PriceDatabase(collection_name="UnitTests", client=self.client)
        self.fetcher = TestFetcher(self.db)

    def tearDown(self) -> None:
        self.client.close()

    def test_no_data_case(self):
        self.assertRaises(Exception, self.fetcher._format_cheapest_product_tweet, "2080 TI")

    @staticmethod
    def create_basic_post():
        return {"product_name":  "Cheapest 2080 TI",
                "product_brand": "ASUS",
                "product_type":  "2080 TI",
                "product_price": 900.0,
                "source":        "Vendor",
                "url":           "http://www.vendor.com"}

    def test_only_yesterday_post_case(self):
        yesterday_post = self.create_basic_post()
        yesterday_post["timestamp"] = get_yesterday_datetime()
        self.db.collection.insert_one(yesterday_post)
        self.assertRaises(Exception, self.fetcher._format_cheapest_product_tweet, "2080 TI")

    def test_only_today_post_case(self):
        today_post = self.create_basic_post()
        today_post["timestamp"] = get_today_datetime()
        self.db.collection.insert_one(today_post)
        self.fetcher._format_cheapest_product_tweet("2080 TI")

    def test_yesterday_and_today_post_case(self):
        posts = [self.create_basic_post(), self.create_basic_post()]
        posts[0]["timestamp"] = get_yesterday_datetime()
        posts[1]["timestamp"] = get_today_datetime()
        self.db.collection.insert_many(posts)
        self.fetcher._format_cheapest_product_tweet("2080 TI")
