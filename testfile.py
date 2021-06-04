# -*- coding: utf-8 -*-
#import tetueSrc
import time
from requests import get
from random import choice
import logging
import json
import tetueSrc
import user_management
from datetime import datetime, timedelta
import db2, db

# read_successful, cfg = tetueSrc.get_configuration("vipbot")
# USERNAME = cfg["name"].lower()
# CLIENT_ID = cfg["client_id"]
# TOKEN = "OAuth " + cfg["token"]

with open ('files/config.json', encoding='utf-8') as file:
    data = json.load(file)

def coins(user, *args):
    coins = db2.field("SELECT Coins FROM users WHERE UserID = ?", user)
    print(f"100135110, du besitzt {coins:,} coins.")

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
    # Zwei Listen vergleichen
    # list_1 = ["test 1", "test 2", "test 3"]
    # list_2 = ["test1", "test 1", "test 2"]
    # list_3 = []
    # for element_1 in list_1:
    #     for element_2 in list_2:
    #         if element_1 == element_2:
    #             list_3.append(element_2)
    # print(list_3)
    # list_4 = [element_2 for element_1 in list_1 for element_2 in list_2 if element_1 == element_2]
    # print(list_4)
    # --------------- Quote ----------------
    # quote = choice(open(tetueSrc.get_string_element("tea_butler", "quotes_path"), encoding='utf-8').readlines())

    # print(quote)
    # CMD_TEA_BUTTLER = tetueSrc.get_string_list("tea_butler", "cmd_coffee") + tetueSrc.get_string_list("tea_butler", "cmd_tea")
    # print(CMD_TEA_BUTTLER)
    # --------------- Database ----------------
    # user_management.update_user_awards()
    # print(user_management.user_awards)
    # test = ["test", "lala", None]
    # print(test)
    # test2 = [element for element in ["test", "lala", None] if (element != None)]
    # print(test2)
    # pass

    # print(datetime.today())
    # print(datetime.now())
    # print(datetime.today().strftime("%Y-%m-%d %H:%M"))

    # Prufe ob man mit mehreren zugriffen auf die Datenbank kommt
    # coins("206130928")
    # coinlock = (datetime.today() + timedelta(seconds=60)).strftime("%Y-%m-%d %H:%M:%S")
    # db2.execute("UPDATE users SET Coins = Coins + ?, CoinLock = ? WHERE UserID = ?", 1, coinlock, "206130928")
    # coins("206130928")
    # db2.commit()
    # db2.close()
    """
    vip_user = db.records("SELECT UserID, MessagesSent, CountLogins, row_number() OVER(ORDER BY Warnings ASC, CountLogins DESC, LoyaltyPoints DESC, Coins DESC) as NoId FROM users WHERE UserID != 206130928 AND UserID != 100135110")
    print(vip_user)
    for element in vip_user:
        if element[0] == "415494080":
            print(f'Da ist er an Position: {element[3]}')
            break
    """
    list = ["hallo", "test"]
    element = "test"
    if element not in list: return
    print("yes")

    for element in range(0, 21, 2):
        print(element)

    print(7+6)

    print("7"+"6")

if __name__ == "__main__":
    main()
