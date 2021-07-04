import db, cmds, misc
import tetueSrc

read_successful, cfg = tetueSrc.get_configuration("bot")
OWNER = cfg["owner"]

warning_timers = (1, 5, 60)


def delete_hashtag(bot, user, call, *args):
    if ("".join(args)) in misc.hashtag_tweet_list:
        misc.hashtag_tweet_list.remove("".join(args))
        bot.send_message(f'Hashtag {"".join(args)} wurde gelöscht.')


def set_games_on(bot, user, call, *args):
    if user.get_mod_rights() == False and user.get_name() != OWNER: return
    for element in cmds.cmds:
        if element.function_info == "games":
            element.allowed = True


def set_games_off(bot, user, call, *args):
    if user.get_mod_rights() == False and user.get_name() != OWNER: return
    for element in cmds.cmds:
        if element.function_info == "games":
            element.allowed = False


def shoutout(bot, user, call, target=None, *args):
    if user.get_mod_rights() == False and user.get_name() != OWNER: return
    if target is None: return
    clear_username = target.replace("@", "").lower()
    channel_url = f'twitch.tv/{clear_username}'
    dict_channel = tetueSrc.get_dict("shoutout", clear_username)
    if dict_channel:
        bot.send_message(dict_channel["bio"])
    else:
        channel_info = bot.get_extern_channel_info(clear_username)
        if not len(channel_info["users"]): return
        bot.send_message(f'Tüftlies, schaut unbedingt hier mal vorbei: {channel_url}. Bio: {channel_info["users"][0]["bio"]}')



def warn(bot, user, call, target=None, *args):
    if user.get_mod_rights() == False and user.get_name() != OWNER: return
    
    if target is None:
        bot.send_message("You must specify a target.")
    else:
        clear_username = target.replace("@", "")
        warnings = db.field("SELECT Warnings FROM users WHERE UserName = ?", clear_username.lower())

        if warnings is None:
            bot.send_message("Dieser Benutzer hat den Kanal noch nicht besucht.")
        elif warnings < len(warning_timers):
            mins = warning_timers[warnings]
            bot.send_message(f"/timeout {target} {mins}m")
            bot.send_message(f"{target}, du hast einen Timeout bekommen, weil du gegen die Chatregeln verstoßen hast. Die Timeoutlänge beträgt {mins} Minute(n).")

            db.execute("UPDATE users SET Warnings = Warnings + 1 WHERE UserName = ?", clear_username.lower())
        else:
            bot.send_message(f"/ban {target} wiederholter Verstoß.")
            bot.send_message(f"{target}, du wurdest wegen wiederholter Verstöße der Chatregeln aus dem Chat verbannt.")


def remove_warn(bot, user, call, target=None, *args):
    if user.get_mod_rights() == False and user.get_name() != OWNER: return

    if target is None:
        bot.send_message("Bitte gib ein Ziel an.")
    else:
        clear_username = target.replace("@", "")
        warnings = db.field("SELECT Warnings FROM users WHERE UserName = ?", clear_username.lower())
        if warnings == 0:
            bot.send_message(f"{target} hat noch keine Verwarnungen.")
        elif warnings > 0 and warnings <= len(warning_timers):
            db.execute("UPDATE users SET Warnings = Warnings - 1 WHERE UserName = ?", clear_username.lower())
            bot.send_message(f"Verwarnungen von {target} entfernt.")
        else:
            # ToDo: Error abfangen
            pass