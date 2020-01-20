BestDeal Project
=======================

Easily compare your most wanted products among your favorite vendors to buy cheapest.

Currently it implements a comparator of NVidia graphic cards among multiple hardware vendors.

<img src='https://github.com/RichardDally/BestDeal/blob/master/screenshots/GTX2080_20181202.png' style='width:334px; height:306px; float: right;'>

BestDeal provides you a visualization tool to anticipate best timing to buy.

### Continuous Integration and code quality

Master branch:


[![Build Status](https://travis-ci.org/RichardDally/BestDeal.svg?branch=master)](https://travis-ci.org/RichardDally/BestDeal)

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/09178071e8a8453fa2acc6d47a4937aa)](https://www.codacy.com/manual/RichardDally/BestDeal?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=RichardDally/BestDeal&amp;utm_campaign=Badge_Grade)


### Requirements

[Python 3.6+](https://www.python.org/downloads/)

[External modules (requirements)](requirements.txt)

[How to install requirements with pip ?](https://stackoverflow.com/a/39537053/5037799)

Usage
-------------
1. Run nvidia_fetcher.py to feed price database (powered by [MongoDB](https://docs.mongodb.com)).
2. Run frontend.py to run a local web server displaying prices graph.
3. Analyze and profit !


MongoDB basics
-------------

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


Backend
-------------

First class to start with is AbstractFetcher.
`continuous_watch` function is convenient function to start fetching and storing data.
It will repeatly calls two functions:
`_scrap_and_store()` fetches, parses and stores product details (price, product type..) in MongoDB (I'm fed up of queries maintenance).
`_display_best_deals()` find best prices for each product type.

An example of AbstractFetcher currently implemented is focused on NVidia GPU from EU hardware vendors.

Implementing a new fetcher is easy:
1) Implement `get_source_product_urls` that returns source names and urls that we want to parse.
2) Implement `_extract_product_data` that returns a Tuple composed of brand and product_type (e.g. "ASUS" and "2080 TI" for Nvidia) from scrapped product description .

### Frontend

:warning: Currently broken, any idea/PR are welcome to help analyze scrapped data.

[Frontend](https://github.com/RichardDally/BestDeal/blob/master/frontend.py) uses [Dash](https://plot.ly/products/dash/) to display beautiful and customizable graphs.
