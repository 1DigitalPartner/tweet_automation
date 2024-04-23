from pydantic import BaseModel
from typing import Optional
import tweepy
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv()


def post_tweet(tweet):
    client = tweepy.Client(consumer_key=os.getenv("CONSUMER_KEY"),
                           consumer_secret=os.getenv("CONSUMER_SECRET"),
                           access_token=os.getenv("ACCESS_KEY"),
                           access_token_secret=os.getenv("ACCESS_SECRET_KEY"))
    client.create_tweet(text=tweet)


class TweetInput(BaseModel):
    tweet: str


class TweetOutput(BaseModel):
    success: bool
    message: Optional[str]
