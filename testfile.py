# -*- coding: utf-8 -*-
import tetueSrc
from requests import get
from random import choice

read_successful, cfg = tetueSrc.get_configuration("vipbot")
USERNAME = cfg["name"].lower()
CLIENT_ID = cfg["client_id"]
TOKEN = "OAuth " + cfg["token"]

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

    # config 'custom-reward-id': '5f4a599a-0133-4226-9eea-d5d2d53b9a4e'
    # namelist = tetueSrc.get_string_list("huehnername","name")
    # print(choice(namelist))
    test_string = "#pog das wird ein hash für den tweet"
    string_1 = test_string.split(" ")[0].lower()
    print(string_1)

    list = ["test","test 2", "test 3"]
    temp_string =  " ".join(list)
    print(temp_string)

if __name__ == "__main__":
    main()
