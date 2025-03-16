import os
from dotenv import load_dotenv
load_dotenv()
from atproto import Client, models

class BlueskyClient:
    def __init__(self, username, password):
        self.client = Client()
        self.client.login(username, password)

    def post(self, text):
        post = self.client.send_post(text)
        return post

    def get_mentions(self,limit=20, cursor=None):
        mentions = self.client.app.bsky.notification.list_notifications(params={"limit":limit,"cursor":cursor})
        return {
            "mentions": mentions,
            "next_cursor": mentions.cursor
        }

    def comment(self,post_uri,post_cid,text):

        root_post_ref = models.ComAtprotoRepoStrongRef.Main(
            uri=post_uri,
            cid=post_cid
        )
        reply = self.client.send_post(
            
            text=text,
            reply_to=models.AppBskyFeedPost.ReplyRef(parent=root_post_ref, root=root_post_ref),
        )
        
        return reply


        

