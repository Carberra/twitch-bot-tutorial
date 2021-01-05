from collections import defaultdict

import db

CURSES = ("bum", "poo", "you are bad")
warning_timers = (1, 5, 60)

def clear(bot, user, message):
    if any([curse in message for curse in CURSES]):
        warn(bot, user, reason="Cursing")
        return False
    return True

def warn(bot, user, *, reason=None):
    warnings = db.field("SELECT Warnings FROM users WHERE UserID = ?", user.get_id())

    if warnings < len(warning_timers):
        mins = warning_timers[warnings]
        bot.send_message(f"/timeout {user.get_displayname()} {mins}m")
        bot.send_message(f"{user.get_displayname()}, you have been muted for the following reason: {reason}. You will be unmuted in {mins} minute(s).")

        db.execute("UPDATE users SET Warnings = Warnings + 1 WHERE UserID = ?", user.get_id())

    else:
        bot.send_message(f"/ban {user.get_displayname()} Repeated infractions.")
        bot.send_message(f"{user.get_displayname()}, you have been banned from chat for repeated infractions.")