BestDeal
=======================

Compare your most wanted products among your favorite vendors to buy cheapest.<br>
Currently it implements a comparator of GPU and CPU among multiple European hardware vendors.<br>

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/richarddally/bestdeal)

[![Build Status](https://travis-ci.org/RichardDally/BestDeal.svg?branch=master)](https://travis-ci.org/RichardDally/BestDeal) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/09178071e8a8453fa2acc6d47a4937aa)](https://www.codacy.com/manual/RichardDally/BestDeal?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=RichardDally/BestDeal&amp;utm_campaign=Badge_Grade)


### Requirements

- [Python 3.6+](https://www.python.org/downloads/)
- [Production requirements](requirements.txt)
- [Development requirements](requirements.dev.txt)
- [How to install requirements with pip ?](https://stackoverflow.com/a/39537053/5037799)

### Usage

#### Looking for GPU or CPU ?

1. Create your [.env file](https://github.com/theskumar/python-dotenv) containing MongoDB credentials (e.g. MONGODB_CONNECTION_STRING=mongodb://localhost:27017)
2. Run cpu_fetcher.py or gpu_fetcher.py to feed price database (powered by [MongoDB](https://docs.mongodb.com)).
3. Analyze and profit !

### MongoDB basics

List all databases:

    > show dbs

Switch to `PriceHistorization` database:

    > use PriceHistorization

Show some statistics:

    > db.stats()

Display every documents:

    > db.NVidiaGPU.find()

Filtering on timestamp:

    > db.NVidiaGPU.find({"product_brand": "GIGABYTE", "timestamp": /20191130_181011/})


### Backend

First class to start with is AbstractFetcher.
`continuous_watch` function is convenient function to start fetching and storing data.

It will repeatly calls two functions:
`_scrap_and_store()` fetches, parses and stores product details (price, product type..) in MongoDB (I'm fed up of queries maintenance).
`_display_best_deals()` find best prices for each product type.

An example of AbstractFetcher currently implemented is focused on NVidia GPU from EU hardware vendors.

Implementing a new fetcher is easy:
1) Implement `get_source_product_urls` that returns source name class and associated urls that we want to parse.
2) Implement `_extract_product_data` that returns a Tuple composed of brand and product_type (e.g. "ASUS" and "2080 TI" for Nvidia) from scrapped product description .
3) Create a new class (inherited from Source) that will implements `_enrich_deals_from_soup` (currently using BeautifulSoup)

### Publish on Twitter

Create a text file named `.env` containing your [Twitter app](https://developer.twitter.com/en/apps/) credentials

    TWITTER_API_KEY="XXXX"
    TWITTER_SECRET_KEY="XXXX"
    TWITTER_ACCESS_TOKEN="XXXX"
    TWITTER_TOKEN_SECRET="XXXX"

Play with publish.py module

### Frontend

