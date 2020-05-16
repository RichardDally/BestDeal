import re
from datetime import datetime, timezone, timedelta


# Full emoji list (for Twitter usage):
# http://www.unicode.org/emoji/charts/full-emoji-list.html

def get_first_place_medal_emoji() -> str:
    return "\U0001F947"


def get_see_no_evil_monkey_emoji() -> str:
    return "\U0001F648"


def get_money_mouth_face_emoji() -> str:
    return "\U0001F911"


def get_euro_banknote_emoji() -> str:
    return "\U0001F4B6"


def get_link_emoji() -> str:
    return "\U0001F517"


def get_canada_emoji() -> str:
    return "\U0001F1E6"


def get_lizard_emoji() -> str:
    return "\U0001F98E"


def get_rightwards_arrow() -> str:
    return "\U000027A1"


def get_south_east_arrow() -> str:
    return "\U00002198"


def get_north_east_arrow() -> str:
    return "\U00002197"


def get_yesterday_date() -> str:
    return datetime.strftime(datetime.now(timezone.utc) - timedelta(1), "%Y%m%d")


def convert_datetime_to_date(date_time: str) -> str:
    """ Example: 20200515_130607 to 2020/05/15 """
    return datetime.strptime(date_time, '%Y%m%d_%H%M%S').strftime('%Y/%m/%d')


def get_today_date() -> str:
    return datetime.now(timezone.utc).strftime('%Y%m%d')


def get_yesterday_datetime() -> str:
    return datetime.strftime(datetime.now(timezone.utc) - timedelta(1), "%Y%m%d_%H%M%S")


def get_today_datetime() -> str:
    return datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')


def clean_price(dirty_price):
    """
    Clean the price to facilitate comparisons.
    I've picked dot as decimal separator (e.g. 42.359€)
    Note every prices are supposed to be in euros, multi currencies is not implemented.
    See clean_price_test module for example cases.
    """
    # Handle Mindfactory case: 1.167,83€ (dot is cosmetic separator, comma is the real separator.)
    if "." in dirty_price and "," in dirty_price:
        dirty_price = dirty_price.replace(".", "")
    dirty_price = dirty_price.replace(' ', '')
    m = re.search('([0-9]+)[€.,]+([0-9]+)', dirty_price)
    return '{}.{}'.format(m.group(1), m.group(2))
