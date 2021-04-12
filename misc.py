from datetime import timedelta, datetime
from sys import exit
from time import time
import tetueSrc
import db, user_management, react

read_successful, cfg = tetueSrc.get_configuration("bot")
OWNER = cfg["owner"]
TWEETMAXLENGTH = tetueSrc.get_int_element("general", "hashtag_max_length")
TWEETWELCOME = tetueSrc.get_string_element("general", "tweet_welcome")
TWEETMINSIZE = tetueSrc.get_int_element("general", "hashtag_min_size")
hashtag_tweet_list = {"#twitchstreamer", "#TwitchDE", "#knorzen"}

def bye(bot, user, *args):
    react.say_goodbye(bot, user)

def lurk(bot, user, *args):
    if user_management.is_user_id_active(user.id) == True:
        bot.send_message(f"Vielen dank fürs mittüfteln {user.get_displayname()} und viel Spaß Im Lurk.")
        user_management.set_user_inactive(user.id)

def hug(bot, user, call, *args):
    if len(args) > 1: return
    if len(args) < 1:
        bot.send_message(f"{user.get_displayname()} nimmt sich selbst in den Arm <3 VirtualHug")
    else:
        clear_username = args[0].replace("@", "")
        if user_management.is_user_name_active(clear_username.lower()) == True:
            bot.send_message(f"{user.get_displayname()} nimmt {clear_username} ganz fest in den Arm <3")

def pogopuschel(bot, user, *args):
    bot.send_message(40*"VirtualHug ")

def hype(bot, user, *args):
     bot.send_message(tetueSrc.get_string_element("outputtext", "hype"))

def modlove(bot, user, *args):
    bot.send_message(tetueSrc.get_string_element("outputtext", "modlove"))

def lostcounter(bot, user, call, *args):
    if len(args) < 1:
        db.execute("UPDATE users SET LostCounter = LostCounter + 1 WHERE UserName = ?", user.get_name())
    elif len(args) > 1:
        bot.send_message(f"{user.get_displayname()}, bitte nach dem Kommando nur ein Argument übergeben.")
    else:
        clear_username = args[0].replace("@", "").lower()
        if user_management.is_user_name_active(clear_username) == True:
            db.execute("UPDATE users SET LostCounter = LostCounter + 1 WHERE UserName = ?", clear_username.lower())
        # else:
        #     bot.send_message(f"Lieber {user.get_displayname()}, der user {args[0]} existiert nicht oder befindet sich im Lurk.")

def state(bot, user, call, *args):
    if len(args) < 1: return
    output_text = tetueSrc.get_string_element("outputtext", args[0].lower())
    if output_text == "": return
    bot.send_message(output_text)

def win(bot, user, *args):
    dict = bot.get_channel_info()
    db.execute("INSERT OR IGNORE INTO category (Category, Wins, Loses) VALUES (?, ?, ?)", dict["Game"], 0, 0)
    db.execute("UPDATE category SET Wins = Wins + 1 WHERE Category = ?", dict["Game"])
    react.update_KD_Counter(bot)

def lose(bot, user, *args):
    dict = bot.get_channel_info()
    db.execute("INSERT OR IGNORE INTO category (Category, Wins, Loses) VALUES (?, ?, ?)", dict["Game"], 0, 0)
    db.execute("UPDATE category SET Loses = Loses + 1 WHERE Category = ?", dict["Game"])
    react.update_KD_Counter(bot)

def register_hastag(bot, user, hashtag, *args):
    global hashtag_tweet_list
    if len(hashtag) < TWEETMINSIZE: return
    if len(TWEETWELCOME + " " + " ".join(hashtag_tweet_list) + " " + hashtag) <= TWEETMAXLENGTH:
        hashtag_tweet_list.add(hashtag)
        print(hashtag_tweet_list)
    else:
        bot.send_message(f'Hashtag nicht registriert. {user.get_displayname()}, es bleiben nur noch {str(TWEETMAXLENGTH - len(TWEETWELCOME + " " + " ".join(hashtag_tweet_list)))} Zeichen übrig zum tweeten.')

def reminder(bot, user, call, *args):
    with open(tetueSrc.get_string_element("paths", "reminderfile"), "a") as f:
        f.write(f'{datetime.today()}: {" ".join(args)}\n')

def help(bot, prefix, cmds):
    bot.send_message(f"Registrierte Befehle: "
        + ", ".join([f"{prefix}{cmd.callables[0]}" for cmd in sorted(cmds, key=lambda cmd: cmd.callables[0])]))

def shutdown(bot, user, *args):
    if user.get_name() == OWNER:
        if not hashtag_tweet_list:
            bot.send_message("Danke für den tollen Stream Tüftlies. Bis zum nächsten Mal.")
        else:
            bot.send_message(TWEETWELCOME + " " + " ".join(hashtag_tweet_list))
        tetueSrc.log_header_info("Stream-Ende")
        db.commit()
        db.close()
        bot.disconnect()
        exit(0)
    else:
        bot.send_message("Du kannst diesen Befehl nicht ausführen.")