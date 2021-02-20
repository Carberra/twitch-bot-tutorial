from datetime import timedelta
from sys import exit
from time import time
import tetueSrc
import db, user_management, react

BOOT_TIME = time()
read_successful, cfg = tetueSrc.get_configuration("bot")
OWNER = cfg["owner"]

def bye(bot, user, *args):
    react.say_goodbye(bot, user)

def lurk(bot, user, *args):
    if user_management.is_user_id_active(user.get_id()) == True:
        bot.send_message(f"Vielen dank fürs mittüfteln {user.get_displayname()} und viel Spaß Im Lurk.")
        user_management.set_user_inactive(user.get_id())

def love(bot, user, *args):
    bot.send_message(40*"VirtualHug ")

def lostcounter(bot, user, *args):
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

def help(bot, prefix, cmds):
    bot.send_message(f"Registrierte Befehle: "
        + ", ".join([f"{prefix}{cmd.callables[0]}" for cmd in sorted(cmds, key=lambda cmd: cmd.callables[0])]))

def shutdown(bot, user, *args):
    if user.get_name() == OWNER:
        bot.send_message("Herunterfahren")
        db.commit()
        db.close()
        bot.disconnect()
        exit(0)

    else:
        bot.send_message("Du kannst diesen Befehl nicht ausführen.")