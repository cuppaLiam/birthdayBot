import requests
import os
from dotenv import load_dotenv
from datetime import datetime

today = datetime.now()
date = today.strftime("%m-%d")  #date in MM-DD format because birthdays are stored with different years
date = "12-15"
load_dotenv()

#Notion stuff
NOTION_TOKEN = os.getenv('NOTION_TOKEN')
DATABASE_ID = os.getenv('DATABASE_ID')

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

#Discord stuff
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

people = []

HR_discord_id = '732146103268540458'


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
    last_day = page["properties"]['Last day at MAC']["date"]
    if last_day != None and datetime.strptime(last_day["start"], "%Y-%m-%d").date() > today.date(): #if last day is set to None, then assume they are still in MAC (as it has not been put in the db yet)
        continue #not an active member
    bday = page["properties"]["Birthday"]["date"]
    if bday == None:
        continue
    elif bday["start"][-5:] == date:
        people.append(page["properties"]["Name"]["title"][0]["text"]["content"])

#send out a message for every person that has a birthday!
for person in people:
    data = {
            "content": "<@&{HR_discord_id}>",
            "embeds": [
                 {
                     "title": "Birthday Alert!",
                     f"description": "Today is {person}'s birthday!",
                     "color": 0xffe430
                }
           ] 
    }
    response = requests.post(WEBHOOK_URL, json=data)
    #print(response.status_code)     
