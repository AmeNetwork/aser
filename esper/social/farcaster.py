import os
from farcaster import Warpcast
import requests



class FarcasterClient:
    def __init__(self):
        self.warpcast = Warpcast(mnemonic=os.getenv("FARCASTER_MNEMONIC"))

    def post(self, text):
        response = self.warpcast.post_cast(text=text)
        return response

    def get_mentions( self, count=10, pagination_token=None):
      
        fid=self.warpcast.get_me().fid
        params={
            "fid":fid,
            "pageSize":count,
            "reverse":1,
            "pageToken":pagination_token
        }
        response=requests.get(f"{os.getenv('FARCASTER_HUBBLE_URL')}/v1/castsByMention",params=params)
        return response.json()
    
    def get_cast(self,cast_id):
        cast=self.warpcast.get_cast(hash=cast_id)
        return cast

    def comment(self,fid,hash,text):
        parent={
            "fid":fid,
            "hash":hash
        }
        response=self.warpcast.post_cast(parent=parent, text=text)
        return response
    
