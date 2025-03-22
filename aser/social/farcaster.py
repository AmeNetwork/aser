import os
from dotenv import load_dotenv
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from eth_account.account import Account
import time
import canonicaljson
import base64
from eth_account.messages import encode_defunct
Account.enable_unaudited_hdwallet_features()
load_dotenv()


class FarcasterClient:
    def __init__(self,mnemonic,access_token=None):

        self.base_path="https://api.warpcast.com/v2/"

        self.wallet = Account.from_mnemonic(mnemonic)
        self.access_token=access_token
        self.rotation_duration=10
        self.expires_at = None
        self.session = requests.Session()
        self.session.mount(
            self.base_path,
            HTTPAdapter(
                max_retries=Retry(
                    total=2, backoff_factor=1, status_forcelist=[520, 413, 429, 503]
                )
            ),
        )
        if self.access_token:
            self.session.headers.update(
                {"Authorization": f"Bearer {self.access_token}"}
            )
            if not self.expires_at:
                self.expires_at = 33228645430000  # 3000-01-01

        elif not self.wallet:
            raise Exception("No wallet or access token provided")
        else:
            self._create_new_auth_token(expires_in=self.rotation_duration)
      

    def post(self, text):
        response = self.post_cast(text=text)
        return response

    def get_mentions( self, count=10, pagination_token=None):
      
        fid=self._get("me")["result"]["user"]["fid"]
        params={
            "fid":fid,
            "pageSize":count,
            "reverse":1,
            "pageToken":pagination_token
        }
        response=requests.get(f"{os.getenv('FARCASTER_HUBBLE_URL')}/v1/castsByMention",params=params)
        return response.json()

    def comment(self,fid,hash,text):
        parent={
            "fid":fid,
            "hash":hash
        }
        response=self.post_cast(parent=parent, text=text)
        return response

    def _get(
        self,
        path,
        params=None,
        json=None,
        headers=None,
    ):
        self._check_auth_header()

        response = self.session.get(
            self.base_path + path, params=params, json=json, headers=headers
        ).json()
        if "errors" in response:
            raise Exception(response["errors"])  # pragma: no cover
        return response    


    def _create_new_auth_token(self, expires_in = 10) -> str:
        now = int(time.time())
        auth_params = {
            "timestamp": now * 1000,
            "expires_at": (now + (expires_in * 60)) * 1000
        }

        body = {
            "method": "generateToken",
            "params": auth_params
        }

        header = self._generate_custody_auth_header(body)
        response = requests.put(
             self.base_path+"auth",
            json=body,  
            headers={"Authorization": header},
        ).json()


        self.access_token = response['result']['token']['secret']
        self.expires_at = auth_params['expires_at']
        self.rotation_duration = expires_in

        self.session.headers.update({"Authorization": f"Bearer {self.access_token}"})

        return self.access_token



    def _generate_custody_auth_header(self, payload: dict) -> str:
        if not self.wallet:
            raise Exception("Wallet not set")
        
        encoded_payload = canonicaljson.encode_canonical_json(payload)
        signable_message = encode_defunct(primitive=encoded_payload)
        signed_message = self.wallet.sign_message(signable_message)
        data_hex_array = bytearray(signed_message.signature)
        encoded = base64.b64encode(data_hex_array).decode()
        return f"Bearer eip191:{encoded}"

    def post_cast(
        self,
        text,
        embeds=None,
        parent=None,
        channel_key=None,
    ):
        body = {
            "text": text,
            "embeds": embeds,
            "parent": parent,
            "channel_key": channel_key
        }
        
        body = {k: v for k, v in body.items() if v is not None}
        
        response = self._post(
            "casts",
            json=body,
        )
        return response.get("result") 

    def _post(
        self,
        path,
        params=None,
        json=None,
        headers=None,
    ) :
        self._check_auth_header()

        response = self.session.post(
            self.base_path + path, params=params, json=json, headers=headers
        ).json()
        if "errors" in response:
            raise Exception(response["errors"])  # pragma: no cover
        return response

    def _check_auth_header(self):
        assert self.expires_at
        if self.expires_at < int(time.time() * 1000)+ 1000:
            self.create_new_auth_token(expires_in=self.rotation_duration)


    
    


