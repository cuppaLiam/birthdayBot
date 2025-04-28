import requests
import os
from dotenv import load_dotenv
from datetime import datetime

today = datetime.now()
date = today.strftime("%m-%d")  #date in MM-DD format because birthdays are stored with different years
load_dotenv()

NOTION_TOKEN = os.getenv('NOTION_TOKEN')
DATABASE_ID = os.getenv('DATABASE_ID')

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def get_pages():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    get_all = True   #ensures all data is collected 
    page_size = 150  #will need to be increased if no. MAC members exceeds 150

    payload = {"page_size": page_size}
    response = requests.post(url, json=payload, headers=headers)

    data = response.json()
    results = data["results"]
    while data["has_more"] and get_all:
        payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
        url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        results.extend(data["results"])
    return results


pages = get_pages()
for page in pages:
    bday = page["properties"]["Birthday"]["date"]
    if bday == None:
        continue
    elif bday["start"][-5:] == date:
        print(page["properties"]["Name"]["title"][0]["text"]["content"])
    
