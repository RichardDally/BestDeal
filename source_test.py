import pytest
from gpu_fetcher import GpuFetcher
from topachat import TopAchat


@pytest.mark.parametrize("fetcher_class", [GpuFetcher])
@pytest.mark.parametrize("source_class", [TopAchat])
def test_source(fetcher_class, source_class):
    """
    Smoke test
    """
    fetcher = fetcher_class(database=None)
    fetcher._scrap_and_store()
