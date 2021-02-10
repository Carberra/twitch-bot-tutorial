from random import choice, randint
from time import time

import db

heist = None
heist_lock = time()

def coinflip(bot, user, side=None, *args):
    if side is None:
        bot.send_message("Du musst raten, auf welcher Seite die Münze landen wird.")
    elif (side := side.lower()) not in (opt := ("k", "z", "kopf", "zahl")):
        bot.send_message("Gib einer der folgenden Seiten ein: " + ", ".join(opt))
    else:
        result = choice(("kopf", "zahl"))
        if side[0] == result[0]:
            db.execute("UPDATE users SET Coins = Coins + 50 WHERE UserID = ?", user.get_id())
            bot.send_message(f"Es ist auf {result} gelandet. Du hast 50 coins gewonnen.")
        else:
            bot.send_message(f"Die Münze ist auf {result} gelandet. Du hast nichts gewonnen.")
