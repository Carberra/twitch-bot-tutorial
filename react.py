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
    
    if user_management.is_user_id_active(user.get_id()) == False:
        welcome(bot, user)
    else:
        for element in emotes_another_world:
            if element in message.lower():
                bot.send_message(f"Was @{user.get_displayname()} meint ist SeemsGood und ist ein Emote aus einer anderen Welt!")
                break

    check_activity(bot, user)

    if (match := search(r'cheer[0-9]+', message)) is not None:
        thank_for_cheer(bot, user, match)

    if (h := games.heist) is not None:
        if h.start_time <= time() and not h.running:
            games.run_heist(bot)

        elif h.end_time <= time() and h.running:
            games.end_heist(bot)

def add_user(bot, user):
    db.execute("INSERT OR IGNORE INTO users (UserID, UserName) VALUES (?, ?)", user.get_id(), user.get_name())

def update_records(bot, user):
    db.execute("UPDATE users SET UserName = ?, MessagesSent = MessagesSent + 1 WHERE UserID = ?", user.get_name(), user.get_id())
    #lastLoginTime = db.field("SELECT LastLogin FROM users WHERE UserID = ?", user.get_id())
    #test = datetime.strptime(lastLoginTime, "%Y-%m-%d %H:%M:%S")
    #print(test)
    # print(type(test))
    # print(datetime.strptime(test, "%Y-%m-%d"))
    #print(datetime.today())
    stamp = db.field("SELECT CoinLock FROM users WHERE UserID = ?", user.get_id())
    if datetime.strptime(stamp, "%Y-%m-%d %H:%M:%S") < datetime.utcnow():
        coinlock = (datetime.utcnow()+timedelta(seconds=60)).strftime("%Y-%m-%d %H:%M:%S")
        db.execute("UPDATE users SET Coins = Coins + ?, CoinLock = ? WHERE UserID = ?", randint(1, 5), coinlock, user.get_id())

def welcome(bot, user):
    if user.get_status() == "moderator":
        bot.send_message(f"Willkommen im Stream {user.get_displayname()}. Die Macht ist mit dir!")
    elif user.get_status() == "vip":
        bot.send_message(f"Willkommen im Stream {user.get_displayname()}. Belehre mich!")
    elif user.get_status() == "broadcaster":
        bot.send_message(f"Das du da bist is klar {user.get_displayname()}. Bau bitte heute mal zur Abwechslung keinen Mist!")
    else:
        bot.send_message(f"Willkommen im Stream {user.get_displayname()}. Viel Spaß beim mittüfteln.")
    user_management.set_user_active(user)

def say_goodbye(bot, user):
    if user_management.is_user_id_active(user.get_id()) == True:
        bot.send_message(f"Vielen dank fürs mittüfteln {user.get_displayname()}. Bis zum nächsten Mal.")
        user_management.set_user_inactive(user.get_id())

def check_activity(bot, user):
    messages[user.get_id()] += 1
    # if (count := messages[user.get_id()]) % 3 == 0:
    # 	bot.send_message(f"Thanks for being active in chat {user.get_displayname()} - you've sent {count:,} messages! Keep it up!")

def thank_for_cheer(bot, user, match):
    bot.send_message(f"Thanks for the {match.group[5:]:,} bits {user.get_displayname()}! That's really appreciated!")