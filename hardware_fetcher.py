from dotenv import load_dotenv
from cpu_fetcher import CpuFetcher
from nvidia_fetcher import NVidiaFetcher
from pricedatabase import PriceDatabase


class HardwareFetcher:
    def __init__(self):
        load_dotenv()
        gpu_db = PriceDatabase(collection_name="NVidiaGPU")
        self.gpu_fetcher = NVidiaFetcher(gpu_db)
        cpu_db = PriceDatabase(collection_name="CPU")
        self.cpu_fetcher = CpuFetcher(cpu_db)

    def multi_fetch(self):
        self.cpu_fetcher.fetch()
        self.gpu_fetcher.fetch()


if __name__ == "__main__":
    pass
