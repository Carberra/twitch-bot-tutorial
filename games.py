from random import choice, randint
import time
import db

running_competition = None

class User:
    def __init__(self, id):
        self.id = id

class Competition:
    def __init__(self):
        self.activuserlist = []
        self.winninguserlist = []
        self.starttime = time.time()
    def add_user(self, user):
        if not any(element.id == user.id for element in self.activuserlist):
            self.activuserlist.append(user)

def competition():
    global running_competition
    if running_competition == None:
        running_competition = Competition()

def coinflip(bot, user, side=None, *args):
    if side is None:
        bot.send_message("Du musst raten, auf welcher Seite die Münze landen wird.")
    elif (side := side.lower()) not in (opt := ("k", "z", "kopf", "zahl")):
        bot.send_message("Gib einer der folgenden Seiten ein: " + ", ".join(opt))
    else:
        result = choice(("kopf", "zahl"))
        if side[0] == result[0]:
            db.execute("UPDATE users SET Coins = Coins + 50 WHERE UserID = ?", user.id)
            bot.send_message(f"Es ist auf {result} gelandet. Du hast 50 coins gewonnen.")
        else:
            bot.send_message(f"Die Münze ist auf {result} gelandet. Du hast nichts gewonnen.")

def main():
    user1 = User(1)
    user2 = User(2)
    competition()
    running_competition.add_user(user1)
    print(running_competition.activuserlist)
    running_competition.add_user(user1)
    print(running_competition.activuserlist)
    running_competition.add_user(user2)
    print(running_competition.activuserlist)
    print(running_competition.starttime)
    time.sleep(3)
    print(time.time()-running_competition.starttime)

if __name__ == "__main__":
    main()