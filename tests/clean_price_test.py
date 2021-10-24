# coding: utf-8

import unittest
from bestdeal.core.toolbox import clean_price


class TestCleanPrice(unittest.TestCase):
    def setUp(self):
        self.reference_price = '422.45'

    def test_case_1(self):
        self.assertEqual(self.reference_price, clean_price('      422.45   €*'))

    def test_case_2(self):
        self.assertEqual(self.reference_price, clean_price('   ---   422,45   €*'))

    def test_case_3(self):
        self.assertEqual(self.reference_price, clean_price('422€45'))

    def test_case_4(self):
        self.assertEqual(self.reference_price, clean_price('4 22€45'))

    def test_case_5(self):
        self.assertEqual("1167.83", clean_price('€ 1.167,83*'))
