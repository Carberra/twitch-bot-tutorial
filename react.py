from collections import defaultdict
from datetime import datetime, timedelta
from random import randint, choice
from re import search
from time import time

import db, games, user_management, tetueSrc

messages = defaultdict(int)

# "Emote from a another world"
emotes_another_world = ["(y)"]
# K/D Counter
cfg_kd = tetueSrc.get_string_element("paths", "kd")
# Hen name
HENNAME = tetueSrc.get_string_element("hunname", "id")
hen_name_list = []
# Auto-Vip
LOYALITYPOINT_1 = tetueSrc.get_int_element("autovip", "num_loy_point_1")
LOYALITYPOINT_2 = tetueSrc.get_int_element("autovip", "num_loy_point_2")
LOYALITYPOINT_3 = tetueSrc.get_int_element("autovip", "num_loy_point_3")

def process(bot, user, message):
    update_records(bot, user)
    update_loyalty_points(user)

    if user.statusIsActive == False:
        welcome(bot, user) # Willkommensnachricht für den User
        user.statusIsActive = True

    # ToDo: Falscher Platz für diese Abfrage
    for element in emotes_another_world:
        if element in message.lower():
            bot.send_message(f"Was @{user.get_displayname()} meint ist SeemsGood und ist ein Emote aus einer anderen Welt!")
            break

    # if (match := search(r'cheer[0-9]+', message)) is not None:
    #     thank_for_cheer(bot, user, match)

def channel_point(bot, user, message, rewardid):
    global hen_name_list
    if rewardid == HENNAME:
        henname = choice(hen_name_list)
        hen_name_list.remove(henname) 
        db.execute("UPDATE users SET HenName = ? WHERE UserID = ?", henname, user.id)
        bot.send_message(f"@{user.get_displayname()}, dein Hühnername ist: {henname}.")
        user.hunname = henname

def update_records(bot, user):
    # Zähle Nachrichten für lokalen User
    user.count_message()
    #print("Nachrichten in dieser Session: " + str(user.messages))

    # Update DB
    db.execute("UPDATE users SET UserName = ?, MessagesSent = MessagesSent + 1 WHERE UserID = ?", user.get_name(), user.id)

    # earn random coins
    stamp = db.field("SELECT CoinLock FROM users WHERE UserID = ?", user.id)
    if datetime.strptime(stamp, "%Y-%m-%d %H:%M:%S") < datetime.today():
        coinlock = (datetime.today()+timedelta(seconds=60)).strftime("%Y-%m-%d %H:%M:%S")
        db.execute("UPDATE users SET Coins = Coins + ?, CoinLock = ? WHERE UserID = ?", randint(1, 5), coinlock, user.id)


def welcome(bot, user):
    if user.badge == user_management.Badge.Moderator:
        bot.send_message(f"Willkommen im Stream {user.get_displayname()}. Die Macht ist mit dir!")
    elif user.badge == user_management.Badge.AutoVIP:
        bot.send_message(f"Willkommen im Stream {user.get_displayname()}. Wegen deiner Treue hast du den VIP Status erhalten. Belehre mich!")
    elif user.badge == user_management.Badge.ManuVIP:
        bot.send_message(f"Willkommen im Stream {user.get_displayname()}. Belehre mich!")
    elif user.badge == user_management.Badge.Broadcaster:
        bot.send_message(f"Dass du da bist is klar, {user.get_displayname()}. Bau bitte heute mal zur Abwechslung keinen Mist!")
    else:
        dict = bot.get_channel_info()
        dict_game = tetueSrc.get_dict("games", dict["Game"])
        if "welcome" in dict_game:
            bot.send_message(f'Willkommen im Stream {user.get_displayname()}. {dict_game["welcome"]}')
        else:
            bot.send_message(f"Willkommen im Stream {user.get_displayname()}.")

def say_goodbye(bot, user):
    if user_management.is_user_id_active(user.id) == True:
        bot.send_message(f"Vielen dank {user.get_displayname()}. Bis zum nächsten Mal.")
        user_management.set_user_inactive(user.id)

def thank_for_cheer(bot, user, bits):
    if bits != "1":
        bot.send_message(f"Vielen Dank für die {bits} Bits, {user.get_displayname()} <3 <3 <3. Die kommen in den Topf fürs nächste Projekt.")
    else:
        bot.send_message(f"Vielen Dank für den einen Bit, {user.get_displayname()} <3 <3 <3. Der kommt in den Topf fürs nächste Projekt.")

def update_loyalty_points(user):
    # Loyalty points (maximal 3 Punkte pro Stream)
    # -- 1. Punkt beim Erstanmelden im Stream
    lastLoginTime = db.field("SELECT LastLogin FROM users WHERE UserID = ?", user.id) # get last login date
    conv_lastLoginTime = datetime.strptime(lastLoginTime, "%Y-%m-%d %H:%M:%S") # convert to datetime-obj
    temp_diff_time = datetime.today() - conv_lastLoginTime # diff time
    if temp_diff_time.days >= LOYALITYPOINT_1: # time diff longer then 1 day
        db.execute("UPDATE users SET CountLogins = CountLogins + ?, LastLogin = ? WHERE UserID = ?", 1, datetime.strftime(datetime.today(), "%Y-%m-%d %H:%M:%S"), user.id)
    # -- 2. Punkt nach 50 Nachrichten
    if user.messages == LOYALITYPOINT_2:
        db.execute("UPDATE users SET LoyaltyPoints = LoyaltyPoints + 1 WHERE UserID = ?", user.id)
    # -- 3. Punkt wäre nach 100 Nachrichten
    elif user.messages == LOYALITYPOINT_3:
        db.execute("UPDATE users SET LoyaltyPoints = LoyaltyPoints + 1 WHERE UserID = ?", user.id)

def update_KD_Counter(bot):
    try:
        dict = bot.get_channel_info()
        wins = db.field("SELECT Wins FROM category WHERE Category = ?", dict["Game"])
        loses = db.field("SELECT Loses FROM category WHERE Category = ?", dict["Game"])
        dict_game = tetueSrc.get_dict("games", dict["Game"])
        with open(cfg_kd, "w") as f:
            f.write(dict_game["win"] + ": " + str(wins) + "\n" + dict_game["lose"] + ": " + str(loses))
    except Exception:
        with open(cfg_kd, "w") as f:
            f.write("No data")
        print("Fehler beim lesen/schreiben der K/D.")

def create_hen_name_list():
    global hen_name_list
    namelist_f = tetueSrc.get_string_list("hunname","list_name_f") # Read all possible Hen-Names
    namelist_m = tetueSrc.get_string_list("hunname","list_name_m") # Read all possible Hen-Names
    proplist = tetueSrc.get_string_list("hunname","propertie") # Read all possible properties
    hennamelist = db.column("SELECT HenName FROM users WHERE HenName IS NOT NULL") # Get all existing Hen-Names
    # Create list with all possible combinations of names
    hen_name_list_f = [("".join([prop, " ", name])) for name in namelist_f for prop in proplist if (name.lower().startswith(prop[:1])and("".join([prop, " ", name]) not in hennamelist))]
    hen_name_list_m = [("".join([prop, "r ", name])) for name in namelist_m for prop in proplist if (name.lower().startswith(prop[:1])and("".join([prop, " ", name]) not in hennamelist))]
    hen_name_list = hen_name_list_f + hen_name_list_m

def main():
    global hen_name_list
    create_hen_name_list()
    print(hen_name_list)
    pass

if __name__ == "__main__":
    main()