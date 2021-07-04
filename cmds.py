from time import time
import misc, economy, games, mod, tetueSrc, user_management, automod

PREFIXMSG = tetueSrc.get_string_element("general", "prefix_msg")
PREFIXTWE = tetueSrc.get_string_element("general", "prefix_twe")
CMD_TEA_BUTTLER = tetueSrc.get_string_list("tea_butler", "cmd_tea") + tetueSrc.get_string_list("tea_butler", "cmd_coffee")
CMD_HONOR = tetueSrc.get_string_list("feat_honor", "cmd_honor")
CMD_OUTPUTTEXT = tetueSrc.get_string_list("outputtext", "text_cmd")


class Cmd(object):
    def __init__(self, callables, func, function_info, rights = user_management.Badge.Tueftlie, cooldown=0):
        self.callables = callables
        self.func = func
        self.cooldown = cooldown
        self.next_use = time()
        self.allowed = True
        self.function_info = function_info
        self.rights = rights


cmds = [
    #	misc
    Cmd(["delete"], games.stats_delete, "games"),
    Cmd(CMD_OUTPUTTEXT, misc.outputtext, "misc"),
    Cmd(CMD_HONOR, games.honor, "misc"),
    Cmd(["shutdown"], misc.shutdown, "misc"),
    Cmd(["lost", "lostcounter"], misc.lostcounter, "misc", cooldown=5),
    Cmd(["kluk", "klug", "kl", "smart"], misc.smartcounter, "misc", cooldown=5),
    Cmd(["liebe","love"], misc.pogopuschel, "misc"),
    Cmd(["lurch", "lurk", "lörk"], misc.lurk, "misc"),
    Cmd(["bye"], misc.bye, "misc"),
    Cmd(["win"], misc.win, "misc", cooldown=30),
    Cmd(["lose"], misc.lose, "misc", cooldown=30),
    Cmd(["hug"], misc.hug, "misc"),
    Cmd(["reminder", "rm"], misc.reminder, "mod", user_management.Badge.ManuVIP),
    Cmd(["quote","qu"], misc.quote, "mod", user_management.Badge.AutoVIP, cooldown=30),
    #	economy
    Cmd(["coins", "money"], economy.coins, "economy"),
    Cmd(["stats"], economy.statistics, "economy"),

    #	games
    Cmd(["coinflip", "flip"], games.coinflip, "games", cooldown=5),
    #Cmd(["competition"], games.competition, "games"),
    Cmd(CMD_TEA_BUTTLER, games.tea, "games"),

    #	mod
    Cmd(["shoutout", "so"], mod.shoutout, "mod", user_management.Badge.Moderator),
    Cmd(["warn"], mod.warn, "mod"),
    Cmd(["unwarn", "rmwarn"], mod.remove_warn, "mod"),
    Cmd(["gameon"], mod.set_games_on, "mod"),
    Cmd(["gameoff"], mod.set_games_off, "mod"),
    Cmd(["hashdelete","hashd","hd"], mod.delete_hashtag, "mod", user_management.Badge.Moderator),
    Cmd(["hashinfo","hashi","hi"], misc.info_hastag, "mod", user_management.Badge.Moderator)
]


def process(bot, user, message):
    if message.startswith(PREFIXMSG):
        cmd = message.split(" ")[0][len(PREFIXMSG):].lower()
        if len(cmd) <= 1: return
        args = message.split(" ")[1:]
        perform(bot, user, cmd, *args)
    elif message.startswith(PREFIXTWE) and user.badge.value <= user_management.Badge.AutoVIP.value:
        hashtag = message.split(" ")[0]
        args = message.split(" ")[1:]
        misc.register_hastag(bot, user, hashtag, *args)


def perform(bot, user, call, *args):
    if call in ("help", "commands", "cmds"):
        misc.help(bot, PREFIXMSG, cmds)
    else:
        if PREFIXMSG in call: return # Sortiere Nachrichten aus wie <!!!>
        for cmd in cmds:
            if call in cmd.callables:
                if cmd.allowed != True: return # cmd ist gerade nicht erlaubt
                if user.badge.value > cmd.rights.value: return # Darf user das Kommando überhaupt ausführen
                if time() > cmd.next_use:
                    cmd.func(bot, user, call, *args)
                    cmd.next_use = time() + cmd.cooldown
                else:
                    bot.send_message(f"Cooldown ist noch aktiv. Versuch es in {cmd.next_use-time():,.0f} Sekunde(n) noch einmal.")

                return
        if automod.check_spam_cmd(bot, user) == True:
            # bot.send_message(f"{user.get_displayname()}, \"{call}\" ist kein gültiger Befehl.")
            pass
