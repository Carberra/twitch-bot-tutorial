# -*- coding: utf-8 -*-
#import tetueSrc
import time
from requests import get
from random import choice
import logging
import json

# read_successful, cfg = tetueSrc.get_configuration("vipbot")
# USERNAME = cfg["name"].lower()
# CLIENT_ID = cfg["client_id"]
# TOKEN = "OAuth " + cfg["token"]

with open ('files/config.json', encoding='utf-8') as file:
    data = json.load(file)

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

    # -------------- Hashtag Feature --------------
    # test_string = "#pog das wird ein hash für den tweet"
    # string_1 = test_string.split(" ")[0].lower()
    # print(string_1)

    # erster_string = "Hallo zusammen "
    # list = {"#1","#2"}
    # list.add("#2")
    # list.add("#3")
    # temp_string =  " ".join(list)
    # print(erster_string + temp_string)
    # print(len(erster_string + " ".join(list)))
    # # print(len(temp_string))
    # # if len("liste ".join(list)) <= 280:
    # #     print(len("liste ".join(list)))
    # #     print("liste ".join(list))
    # # else:
    # #     print("nein")

    # TWEETMAXLENGTH = 280
    # TWEETWELCOME = "Hallo und"
    # print(len(TWEETWELCOME + " " + " ".join(list)))
    # user = "@TeTü"
    # print(f'{user}, es bleiben nur noch {str(TWEETMAXLENGTH - len(TWEETWELCOME + " " + " ".join(list)))} Zeichen übrig zum tweeten.')

    # -------------- Logging --------------
    # log_format = ('[%(asctime)s] %(levelname)-10s %(message)s')
    # logging.basicConfig(level=logging.DEBUG, format=log_format, filename=('files/debug.log'),)
    # logging.debug('debug')
    # logging.info('info')
    # logging.warning('warning')
    # logging.error('error')
    # logging.critical('critical')

    # --------------- Json ----------------
    # print(json.dumps(data, indent=4)) # Formatierte Ausgabe
    # print(type(data))
    # print(type(data['hunname']['icon']))
    # print(data['hunname']['icon'])
    # if "icon" in data['hunname']:
    #     print("Vorhanden")
    # else:
    #     print("Nicht vorhanden")
    # if "icon" not in data['hunname']:
    #     print("Nicht Vorhanden 2")
    # else:
    #     print("Vorhanden 2")

    # print(data['autovip']['num_max_auto_vips'])
    # print(type(data['autovip']['num_max_auto_vips']))
    # print(type(str(data['autovip']['num_max_auto_vips'])))

    # print(data['games']['Populous: The Beginning']['welcome'])

    pass

if __name__ == "__main__":
    main()
