# -*- coding: utf-8 -*-
import tetueSrc
from requests import get
from random import choice

read_successful, cfg = tetueSrc.get_configuration("vipbot")
USERNAME = cfg["name"].lower()
CLIENT_ID = cfg["client_id"]
TOKEN = "oauth:" + cfg["token"]

def main():
    # Get Channel
    # url = f"https://api.twitch.tv/kraken/channel"
    # headers = {"Client-ID": CLIENT_ID, "Accept": "application/vnd.twitchtv.v5+json", "Authorization": TOKEN}
    # resp = get(url, headers=headers).json()
    # print(resp)

    # Get Channel by ID
    # url = f"https://api.twitch.tv/kraken/users?login={USERNAME}"
    # headers = {"Client-ID": CLIENT_ID, "Accept": "application/vnd.twitchtv.v5+json"}
    # resp = get(url, headers=headers).json()
    # channel_id = resp["users"][0]["_id"]

    # url = f"https://api.twitch.tv/kraken/channels/{channel_id}"
    # headers = {"Client-ID": CLIENT_ID, "Accept": "application/vnd.twitchtv.v5+json"}
    # resp = get(url, headers=headers).json()
    # if not resp:
    #     print("Fehler")
    # else:
    #     print(resp["game"])

    # config
    namelist = tetueSrc.get_string_list("huehnername","name")
    print(choice(namelist))

if __name__ == "__main__":
    main()
