from random import choice, randint
from enum import Enum, auto
import time
import db,user_management

running_competition = None

class Status(Enum):
    Running = auto()
    Stopped = auto()
    Closed = auto()

class Competition:
    def __init__(self):
        self.status = Status.Running
        self.activuserlist = []
        self.winninguserlist = []
        self.starttime = time.time()
    def add_user(self, bot, user):
        if not any(element.id == user.id for element in self.activuserlist) and not any(element.id == user.id for element in self.winninguserlist):
            self.activuserlist.append(user)
            bot.send_message(f"{user.get_displayname()}, du nimmst an der Verlosung teil.")
    def drawing(self, bot):
        if not self.activuserlist: return
        winner = choice(self.activuserlist)
        for element in self.activuserlist:
            if element.id == winner.id:
                self.activuserlist.remove(element)
                self.winninguserlist.append(winner)
                bot.send_message(f"{winner.get_displayname()}, du hast gewonnen! Herzlichen Glückwunsch!")
                return

def competition(bot, user, cmd=None, *args):
    global running_competition
    # Verlosung starten
    if running_competition == None and cmd == "start" and user.badge == user_management.Badge.Broadcaster:
        running_competition = Competition()
    # Verlosung stoppen
    elif running_competition != None and cmd == "ende" and user.badge == user_management.Badge.Broadcaster:
        running_competition.status = Status.Stopped
    # Verlosung beenden
    elif running_competition != None and cmd == "schließen" and running_competition.status == Status.Stopped and user.badge == user_management.Badge.Broadcaster:
        running_competition = None
    # Gewinner ziehen
    elif running_competition != None and cmd == "ziehen" and running_competition.status == Status.Running and user.badge == user_management.Badge.Broadcaster:
        running_competition.drawing(bot)
    # An Verlosung teilnehmen
    elif running_competition != None and running_competition.status == Status.Running:
        running_competition.add_user(bot, user)
    else:
        pass

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
    pass

if __name__ == "__main__":
    main()