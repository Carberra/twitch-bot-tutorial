from random import choice, randint
from time import time

import db

heist = None
heist_lock = time()

def coinflip(bot, user, side=None, *args):
    if side is None:
        bot.send_message("You need to guess which side the coin will land!")
    elif (side := side.lower()) not in (opt := ("h", "t", "heads", "tails")):
        bot.send_message("Enter one of the following as the side: " + ", ".join(opt))
    else:
        result = choice(("heads", "tails"))
        if side[0] == result[0]:
            db.execute("UPDATE users SET Coins = Coins + 50 WHERE UserID = ?", user.get_id())
            bot.send_message(f"It landed on {result}! You won 50 coins!")
        else:
            bot.send_message(f"Too bad - it landed on {result}. You didn't win anything!")
