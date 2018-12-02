BestDeal Project
=======================

Easily compare your most wanted products among your favorite vendors to buy cheapest.

<img src='https://github.com/RichardDally/BestDeal/blob/master/screenshots/GTX2080_20181202.png' style='width:334px; height:306px; float: right;'>

BestDeal provides you a backend and a frontend to decide what's the best moment to buy.

Backend
-------------
Backend is composed of two main modules : deals scrappers and price database.

[Deals scrappers](https://github.com/RichardDally/BestDeal/blob/master/dealscrappers.py) will navigate on vendors page (e.g. Amazon) and scraps product name, type and price to store it in [price database](https://github.com/RichardDally/BestDeal/blob/master/pricedatabase.py) !


Frontend
-------------
[Frontend](https://github.com/RichardDally/BestDeal/blob/master/frontend.py) uses [Dash](https://plot.ly/products/dash/) to display beautiful and customizable graphs.
