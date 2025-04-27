import requests
import os
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.getenv('WEBHOOK_URL')

data = {
        "content": "<@&1363855221209563308>",
        "embeds": [
             {
                 "title": "Birthday Alert!",
                 "description": "Today is _______'s birthday!",
                 "color": 0xffe430
            }
       ] 
}

response = requests.post(WEBHOOK_URL, json=data)

print(response.status_code)
