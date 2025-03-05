import os
import tweepy
class TwitterClient:
    def __init__(self):
        self.client = tweepy.Client(
            bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
            consumer_key=os.getenv("TWITTER_API_KEY"),
            consumer_secret=os.getenv("TWITTER_API_SECRET"),
            access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
            access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
        )

    def post(self, text):
        response = self.client.create_tweet(text=text)
        return response

    def get_mentions(
        self, count=10, pagination_token=None, start_time=None, end_time=None
    ):
        me = self.client.get_me()
        mentions = self.client.get_users_mentions(
            id=me.data["id"],
            max_results=count,
            user_fields=["username"],
            expansions=["author_id"],
            pagination_token=pagination_token,
            start_time=start_time,
            end_time=end_time
        )
        print(mentions)
        return mentions

    def comment(self, tweet_id, text):
        response = self.client.create_tweet(text=text, in_reply_to_tweet_id=tweet_id)
        return
