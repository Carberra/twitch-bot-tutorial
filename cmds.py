from time import time
import misc, economy, games, mod

PREFIX = "!"

class Cmd(object):
    def __init__(self, callables, func, function_info, cooldown=0):
        self.callables = callables
        self.func = func
        self.cooldown = cooldown
        self.next_use = time()
        self.allowed = True
        self.function_info = function_info

cmds = [
    #	misc
    Cmd(["shutdown"], misc.shutdown, "misc"),
    Cmd(["lost", "lostcounter"], misc.lostcounter, "misc", cooldown=5),
    Cmd(["liebe","love"], misc.love, "misc"),
    Cmd(["lurch", "lurk", "lörk"], misc.lurk, "misc"),
    Cmd(["bye"], misc.bye, "misc"),
    Cmd(["text"], misc.text, "misc"),
    Cmd(["win"], misc.win, "misc", cooldown=5),
    Cmd(["lose"], misc.lose, "misc", cooldown=5),
    #Cmd(["bug", "bugcounter"], misc.lostcounter, cooldown=10),

    #	economy
    Cmd(["coins", "money"], economy.coins, "economy"),

    #	games
    Cmd(["coinflip", "flip"], games.coinflip, "games", cooldown=5),
    Cmd(["competition"], games.competition, "games"),


    #	mod
    Cmd(["warn"], mod.warn, "mod"),
    Cmd(["unwarn", "rmwarn"], mod.remove_warn, "mod"),
    Cmd(["gameon"], mod.set_games_on, "mod"),
    Cmd(["gameoff"], mod.set_games_off, "mod")
]

def process(bot, user, message):
    if message.startswith(PREFIX):
        cmd = message.split(" ")[0][len(PREFIX):].lower()
        args = message.split(" ")[1:]
        perform(bot, user, cmd, *args)

def perform(bot, user, call, *args):
    if call in ("help", "commands", "cmds"):
        misc.help(bot, PREFIX, cmds)
    else:
        if PREFIX in call: return # Sortiere Nachrichten aus wie <!!!>
        for cmd in cmds:
            if call in cmd.callables:
                if cmd.allowed != True: return # cmd ist gerade nicht erlaubt
                if time() > cmd.next_use:
                    cmd.func(bot, user, *args)
                    cmd.next_use = time() + cmd.cooldown
                else:
                    bot.send_message(f"Cooldown ist noch aktiv. Versuch es in {cmd.next_use-time():,.0f} Sekunde(n) noch einmal.")

                return
        bot.send_message(f"{user.get_displayname()}, \"{call}\" ist kein gültiger Befehl.")
