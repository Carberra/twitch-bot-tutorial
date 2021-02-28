from collections import defaultdict
from datetime import datetime, timedelta
from random import randint
from re import search
from time import time

import db, games, user_management

# "Emote from a another world"
emotes_another_world = ["(y)"]

messages = defaultdict(int)

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

    if (match := search(r'cheer[0-9]+', message)) is not None:
        thank_for_cheer(bot, user, match)

def update_records(bot, user):
    # Zähle Nachrichten für lokalen User
    user.count_message()
    print("Nachrichten in dieser Session: " + str(user.messages))

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
        bot.send_message(f"Willkommen im Stream {user.get_displayname()}. Wegen deiner Treue hast du einen VIP Status erhalten. Belehre mich!")
    elif user.badge == user_management.Badge.ManuVIP:
        bot.send_message(f"Willkommen im Stream {user.get_displayname()}. Belehre mich!")
    elif user.badge == user_management.Badge.Broadcaster:
        bot.send_message(f"Dass du da bist is klar {user.get_displayname()}. Bau bitte heute mal zur Abwechslung keinen Mist!")
    else:
        bot.send_message(f"Willkommen im Stream {user.get_displayname()}. Viel Spaß beim mittüfteln.")

def say_goodbye(bot, user):
    if user_management.is_user_id_active(user.id) == True:
        bot.send_message(f"Vielen dank fürs mittüfteln {user.get_displayname()}. Bis zum nächsten Mal.")
        user_management.set_user_inactive(user.id)

def thank_for_cheer(bot, user, match):
    bot.send_message(f"Thanks for the {match.group[5:]:,} bits {user.get_displayname()}! That's really appreciated!")

def update_loyalty_points(user):
    # Loyalty points (maximal 3 Punkte pro Stream)
    # -- 1. Punkt beim Erstanmelden im Stream
    lastLoginTime = db.field("SELECT LastLogin FROM users WHERE UserID = ?", user.id) # get last login date
    conv_lastLoginTime = datetime.strptime(lastLoginTime, "%Y-%m-%d %H:%M:%S") # convert to datetime-obj
    temp_diff_time = datetime.today() - conv_lastLoginTime # diff time
    if temp_diff_time.days >= 1: # time diff longer then 1 day
        db.execute("UPDATE users SET CountLogins = CountLogins + ?, LastLogin = ? WHERE UserID = ?", 1, datetime.strftime(datetime.today(), "%Y-%m-%d %H:%M:%S"), user.id)
    # -- 2. Punkt nach 50 Nachrichten
    if user.messages == 50: #ToDo: Grenzen in config schreiben
        db.execute("UPDATE users SET LoyaltyPoints = LoyaltyPoints + 1 WHERE UserID = ?", user.id)
    # -- 3. Punkt wäre nach 100 Nachrichten
    elif user.messages == 100: #ToDo: Grenzen in config schreiben
        db.execute("UPDATE users SET LoyaltyPoints = LoyaltyPoints + 1 WHERE UserID = ?", user.id)

def main():
    # t = timedelta(days = 5, hours = 1, seconds = 33, microseconds = 233423)
    # print("total seconds =", t.total_seconds())
    # print("sec: " + str(t.seconds))
    # print("days: " + str(t.days))
    # print(type(t.days))
    # print(datetime.utcnow())
    # print(datetime.today())

    # print(type(datetime.strptime(datetime.today(), "%Y-%m-%d %H:%M:%S")))
    print(type(datetime.strftime(datetime.today(), "%Y-%m-%d %H:%M:%S")))
if __name__ == "__main__":
    main()
