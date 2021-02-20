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

def warn(bot, user, target=None, *args):
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

def remove_warn(bot, user, target=None, *args):
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