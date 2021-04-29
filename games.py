from random import choice
from enum import Enum, auto
import time
import db,user_management, tetueSrc

TEAANSWERTIME = tetueSrc.get_int_element("tea_butler", "answer_time")
TEAANSWER = tetueSrc.get_string_list("tea_butler", "answer_butler")
TEA_EMOTE = tetueSrc.get_string_element("tea_butler", "emote_tea")
TEA_CMD = tetueSrc.get_string_list("tea_butler", "cmd_tea")
COFFEE_EMOTE = tetueSrc.get_string_element("tea_butler", "emote_coffee")
COFFEE_CMD = tetueSrc.get_string_list("tea_butler", "cmd_coffee")
QUOTESPATH = tetueSrc.get_string_element("tea_butler", "quotes_path")
HONORANSWERTIME = tetueSrc.get_int_element("feat_honor", "answer_time")
HONOR_MIN_DIVISOR = tetueSrc.get_string_list("feat_honor", "divisor")

running_competition = None
running_tea_butler = []
running_time_processes = []

class Status(Enum):
    Running = auto()
    Stopped = auto()
    Closed = auto()

class tea_butler():
    def __init__(self, user):
        self.user_id = user
        self.starttime = time.time()
    def get_lifetime(self):
        return time.time() - self.starttime

class honor_process():
    def __init__(self, nominee_user, bot):
        self.nominee_user = nominee_user
        self.starttime = time.time()
        self.runbot = bot
        self.active_user = set()
        self.chatter_count = self.runbot.get_chatroom_info()["chatter_count"]
    def run(self):
        if self.get_lifetime() > HONORANSWERTIME:
            print(f'Lifetime abgelaufen: {self.chatter_count} durch {HONOR_MIN_DIVISOR} = {self.chatter_count//HONOR_MIN_DIVISOR}')
            if len(self.active_user) >= self.chatter_count//HONOR_MIN_DIVISOR:
                db.execute("UPDATE users SET EhrenCounter = EhrenCounter + 1 WHERE UserName = ?", self.nominee_user)
                self.runbot.send_message(f"Ehre geht raus an {self.nominee_user} mit den supportern: {', '.join(self.active_user)}")
            return False
        return True
    def get_lifetime(self):
        return time.time() - self.starttime

def honor(bot, user, call, *args):
    if len(args) < 1: return # No nominee user
    clear_username = args[0].replace("@", "").lower()
    temp_honor_active = False
    for run_process in running_time_processes:
        if isinstance(run_process, honor_process):
            if run_process.nominee_user == clear_username:
                run_process.active_user.add(user.get_name())
                temp_honor_active = True
                print(run_process.active_user)
                break
    if (user.get_name() == bot.owner) and (temp_honor_active == False):
        nomination = honor_process(clear_username, bot)
        running_time_processes.append(nomination)
        nomination.active_user.add(user.get_name())
        print(running_time_processes)

def run_time_processes():
    global running_time_processes
    for process in running_time_processes[:]:
        if process.run() == False:
            running_time_processes.remove(process)
            print(running_time_processes)

def new_tea(bot, user, call, *args):
    quote_raw = choice(open(tetueSrc.get_string_element("tea_butler", "quotes_path"), encoding='utf-8').readlines())
    quote = quote_raw.replace("\n", "")
    if any(word in call for word in TEA_CMD):
        bot.send_message(f"{TEA_EMOTE} {user.get_displayname()}, bitteschön. {quote}")
    elif any(word in call for word in COFFEE_CMD):
        bot.send_message(f"{COFFEE_EMOTE} {user.get_displayname()}, bitteschön. {quote}")

    running_tea_butler.append(tea_butler(user.id))

def process_tea_butler(bot, user, message):
    for tea in running_tea_butler:
        if tea.get_lifetime() > TEAANSWERTIME:
            running_tea_butler.remove(tea)
        elif tea.user_id == user.id:
            if any(word in message.lower() for word in TEAANSWER):
                bot.send_message(f"{user.get_displayname()}, bitteschön <3")
                running_tea_butler.remove(tea)
                break

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
        bot.send_message(f"Verlosung gestartet.")
    # Verlosung stoppen
    elif running_competition != None and cmd == "ende" and user.badge == user_management.Badge.Broadcaster:
        running_competition.status = Status.Stopped
        bot.send_message(f"Teilnahme an der Verlosung beendet.")
    # Verlosung beenden
    elif running_competition != None and cmd == "schließen" and running_competition.status == Status.Stopped and user.badge == user_management.Badge.Broadcaster:
        running_competition = None
        bot.send_message(f"Verlosung beendet.")
    # Gewinner ziehen
    elif running_competition != None and cmd == "ziehen" and running_competition.status == Status.Running and user.badge == user_management.Badge.Broadcaster:
        running_competition.drawing(bot)
    # An Verlosung teilnehmen
    elif running_competition != None and running_competition.status == Status.Running:
        running_competition.add_user(bot, user)
    else:
        pass

def coinflip(bot, user, call, side=None, *args):
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