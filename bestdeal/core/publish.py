import os
import tweepy
from typing import Optional
from loguru import logger


def get_twitter_api():
    auth = tweepy.OAuthHandler(consumer_key=os.environ.get("TWITTER_API_KEY"),
                               consumer_secret=os.environ.get("TWITTER_SECRET_KEY"))
    auth.set_access_token(key=os.environ.get("TWITTER_ACCESS_TOKEN"),
                          secret=os.environ.get("TWITTER_TOKEN_SECRET"))
    return tweepy.API(auth)


def tweet(text_to_publish: Optional[str]):
    if text_to_publish:
        api = get_twitter_api()
        api.update_status(status=text_to_publish)
    else:
        logger.warning("Nothing to publish...")


if __name__ == "__main__":
    try:
        api = get_twitter_api()
        api.verify_credentials()
        logger.info("Authentication OK")
    except Exception as exception:
        logger.exception(exception)
