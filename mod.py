import db, cmds
import tetueSrc

read_successful, cfg = tetueSrc.get_configuration("bot")
OWNER = cfg["owner"]

warning_timers = (1, 5, 60)

def set_games_on(bot, user, *args):
    if user.get_mod_rights() == False and user.get_name() != OWNER: return
    for element in cmds.cmds:
        if element.get_function_info() == "games":
            element.set_allowed(True)

def set_games_off(bot, user, *args):
    if user.get_mod_rights() == False and user.get_name() != OWNER: return
    for element in cmds.cmds:
        if element.get_function_info() == "games":
            element.set_allowed(False)

def warn(bot, user, target=None, *reason):
    if user.get_mod_rights() == False and user.get_name() != OWNER: return
    
    if target is None:
        bot.send_message("You must specify a target.")
    else:
        clear_username = target.replace("@", "")
        reason = " ".join(reason)
        warnings = db.field("SELECT Warnings FROM users WHERE UserName = ?", clear_username.lower())

        if warnings is None:
            bot.send_message("That user hasn't visitied this channel yet.")
        elif warnings < len(warning_timers):
            mins = warning_timers[warnings]
            bot.send_message(f"/timeout {target} {mins}m")
            bot.send_message(f"{target}, you have been muted for the following reason: {reason}. You will be unmuted in {mins} minute(s).")
            db.execute("UPDATE users SET Warnings = Warnings + 1 WHERE UserName = ?", clear_username.lower())
        else:
            bot.send_message(f"/ban {target} Repeated infractions.")
            bot.send_message(f"{target}, you have been banned from chat for repeated infractions.")

def remove_warn(bot, user, target=None, *args):
    if user.get_mod_rights() == False and user.get_name() != OWNER: return

    if target is None:
        bot.send_message("You must specify a target.")
    else:
        clear_username = target.replace("@", "")
        warnings = db.field("SELECT Warnings FROM users WHERE UserName = ?", clear_username.lower())
        if warnings == 0:
            bot.send_message(f"{target} has not received any warnings.")
        elif warnings > 0 and warnings <= len(warning_timers):
            db.execute("UPDATE users SET Warnings = Warnings - 1 WHERE UserName = ?", clear_username.lower())
            bot.send_message(f"Warning for {target} revoked.")
        else:
            # ToDo: Error abfangen
            pass