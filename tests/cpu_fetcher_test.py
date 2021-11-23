# coding: utf-8

import unittest
from bestdeal.backend.cpu_fetcher import CpuFetcher


class TestExtractProductData(unittest.TestCase):
    def setUp(self) -> None:
        self.fetcher = CpuFetcher(database=None)

    def test_case_1(self):
        product_description = "AMD Ryzen 5 3600X (3.6 GHz) + 3 mois d'abonnement Xbox Game Pass offert !"
        brand, product_type = self.fetcher._extract_product_data(product_description)
        self.assertEqual("AMD", brand)
        self.assertEqual("RYZEN 5 3600X", product_type)

    def test_case_2(self):
        product_description = "AMD Ryzen 5 3600 (3.6 GHz) + AMD Wraith Prism + 3 mois d'abonnement Xbox Game Pass offert ! "
        brand, product_type = self.fetcher._extract_product_data(product_description)
        self.assertEqual("AMD", brand)
        self.assertEqual("RYZEN 5 3600", product_type)

    def test_case_3(self):
        product_description = "AMD Ryzen 5 3600X ~~~~"
        brand, product_type = self.fetcher._extract_product_data(product_description)
        self.assertEqual("AMD", brand)
        self.assertEqual("RYZEN 5 3600X", product_type)


