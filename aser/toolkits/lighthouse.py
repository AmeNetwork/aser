"""
Lighthouse 
learn more about lighthouse: https://docs.lighthouse.storage/
"""
import os
import json
import io
from dotenv import load_dotenv
from lighthouseweb3 import Lighthouse
from aser.tools import tool

load_dotenv()

@tool()
def lighthouse(data: str):
    """this function is used to upload data to lighthouse/IPFS"""
    try:
        lh = Lighthouse(token=os.getenv("LIGHTHOUSE_API_KEY"))
        # json_string = json.dumps(json_data, ensure_ascii=False, indent=2)

        json_file = io.BytesIO(data.encode('utf-8'))

        upload_result = lh.uploadBlob(json_file, "data.md")
        cid=upload_result["data"]["Hash"]

        return f"IPFS LINK: https://gateway.lighthouse.storage/ipfs/{cid}"

    except Exception as e:
        raise Exception(f"upload data to ipfs fail: {str(e)}")






