import os
from dotenv import load_dotenv
from mastodon import Mastodon
load_dotenv()
class MastodonClient:
    def __init__(self):
        self.client = Mastodon(
            access_token = os.getenv('MASTODON_ACCESS_TOKEN'),
            api_base_url = os.getenv('MASTODON_API_BASE_URL'),
        )

    def post(self, text):
        response = self.client.status_post(text)
        return response   

    def get_mentions(self, count=1, since_id=None):
        mentions = self.client.notifications(limit=count, since_id=since_id,mentions_only=True)

        latest_id = mentions[0]['id'] if mentions else None
    
        return mentions, latest_id

    def comment(self, status_id, text):
        response = self.client.status_post(
            status=text,
            in_reply_to_id=status_id
        )
        return response



