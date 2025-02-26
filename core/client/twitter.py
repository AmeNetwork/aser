from dotenv import load_dotenv
import os
import tweepy
load_dotenv()
class TwitterClient:
    def __init__(self):
        self.client=tweepy.Client(
            bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
            consumer_key=os.getenv("TWITTER_API_KEY"),
            consumer_secret=os.getenv("TWITTER_API_SECRET"),
            access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
            access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
        )
    
    def post(self,text):
        response=self.client.create_tweet(text=text)
        print("Tweet posted successfully!", response)
    
    def get_mentions(self,count=10):
        me=self.client.get_me()
        mentions=self.client.get_users_mentions(id=me.data["id"],max_results=count,user_fields=["username"],expansions=["entities.mentions.username"])
        print(mentions)
        return mentions

    def comment(self,in_reply_to_tweet_id,text):
        response=self.client.create_tweet(text=text,in_reply_to_tweet_id=in_reply_to_tweet_id)
        print("Tweet posted successfully!", response)


    
    # def get_me(self):
    #     me=self.client.get_me()
    #     print()
    #     return me
    
