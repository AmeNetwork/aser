import requests
from datetime import datetime, time

def get_web3_news(page=1,size=100):
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
    
blockbeats = [
    {
        "name": "get_web3_news",
        "description": "this function is used to top web3 news, use it when asked about web3 news.", 
        "parameters": {
            "type": "object",
            "properties": {
               
            },
            "required": [],
        },
        "function": get_web3_news,
        "extra_prompt": "Retain all information",
        "example":"today web3 news"
    }
]