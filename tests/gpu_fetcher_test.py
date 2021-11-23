import unittest
from bestdeal.backend.gpu_fetcher import GpuFetcher


class TestFindExactlyOneElement(unittest.TestCase):
    def setUp(self) -> None:
        self.fetcher = GpuFetcher(database=None)

    @unittest.skip("TODO")
    def test_case_1(self):
        brands = ["GAINWARD", "ASUS"]
        product_data = "6GB Gainward GeForce GTX 1660 Pegasus OC Aktiv PCIe 3.0 x16 (Retail)"
        result = self.fetcher.find_exactly_one_element(pattern_data=brands, raw_data=product_data)
        self.assertIsNotNone(result, "GAINWARD brand should be found")


class TestExtractProductData(unittest.TestCase):
    def setUp(self) -> None:
        self.fetcher = GpuFetcher(database=None)

    def test_nvidia_case_1(self):
        product_description = 'Palit GeForce RTX 2080 Ti StormX, 6 Go'
        brand, product_type = self.fetcher._extract_product_data(product_description)
        self.assertEqual('PALIT', brand)
        self.assertEqual('2080 TI', product_type)

    def test_nvidia_case_2(self):
        product_description = 'Zotac Gaming GeForce RTX 2060 AMP Edition, 6 Go + jeu offert ! '
        brand, product_type = self.fetcher._extract_product_data(product_description)
        self.assertEqual('ZOTAC', brand)
        self.assertEqual('2060', product_type)

    def test_nvidia_case_3(self):
        product_description = 'MSI 2060 SuPeR'
        brand, product_type = self.fetcher._extract_product_data(product_description)
        self.assertEqual('MSI', brand)
        self.assertEqual('2060 SUPER', product_type)

    def test_nvidia_case_4(self):
        product_description = 'GIGABYTE GeForce® RTX 2070 D5 4G'
        brand, product_type = self.fetcher._extract_product_data(product_description)
        self.assertEqual('GIGABYTE', brand)
        self.assertEqual('2070', product_type)

    def test_nvidia_case_5(self):
        product_description = 'MSI RTX 3080 Ti 6 Go'
        brand, product_type = self.fetcher._extract_product_data(product_description)
        self.assertEqual('MSI', brand)
        self.assertEqual('3080 TI', product_type)

    def test_nvidia_case_6(self):
        product_description = 'RTX 3070 GAINWARD'
        brand, product_type = self.fetcher._extract_product_data(product_description)
        self.assertEqual('GAINWARD', brand)
        self.assertEqual('3070', product_type)

    def test_nvidia_case_7(self):
        product_description = 'RTX PNY 3080'
        brand, product_type = self.fetcher._extract_product_data(product_description)
        self.assertEqual('PNY', brand)
        self.assertEqual('3080', product_type)

    def test_radeon_case_1(self):
        product_description = "MSI Radeon RX 5700 XT EVOKE OC (v2) + 2 jeux offerts ! "
        brand, product_type = self.fetcher._extract_product_data(product_description)
        self.assertEqual('MSI', brand)
        self.assertEqual('5700 XT', product_type)

    def test_radeon_case_2(self):
        product_description = "ASRock Radeon RX 570 Phantom Gaming D OC (8 Go)"
        brand, product_type = self.fetcher._extract_product_data(product_description)
        self.assertEqual("ASROCK", brand)
        self.assertEqual("570", product_type)
