import requests
from aser.tools import tool
from datetime import datetime, time

@tool()
def blockbeats(page: int = 1, size: int = 100):
    """this function is used to get web3 news, use it when asked about web3 news.
    Args:
        page (int, optional): page number. Defaults to 1.
        size (int, optional): page size. Defaults to 100.
    """
    url = f"https://api.theblockbeats.news/v1/open-api/open-flash?page={page}&size={size}&type=all&lang=cn"
    response = requests.request("GET", url, headers={}, data={})
    today = datetime.now().date()
    today_start = int(datetime.combine(today, time.min).timestamp())
    current_time = int(datetime.now().timestamp())
    filtered_data = [
        f"{item['title']}\n{item['content']}\n"
        for item in response.json()["data"]["data"]
        if today_start <= int(item['create_time']) <= current_time
    ]
    filtered_data_str= "\n".join(filtered_data)
    return filtered_data_str
    