from .. import db

OWNER = "superbootwitch"

warning_timers = (1, 5, 60)


def warn(bot, user, target=None, *reason):
	if target is None:
		bot.send_message("You must specify a target.")

	elif user["name"] == OWNER:
		reason = " ".join(reason)
		warnings = db.field("SELECT Warnings FROM users WHERE UserName = ?",
			target.lower())

		if warnings is None:
			bot.send_message("That user hasn't visitied this channel yet.")

		elif warnings < len(warning_timers):
			mins = warning_timers[warnings]
			bot.send_message(f"/timeout {target} {mins}m")
			bot.send_message(f"{target}, you have been muted for the following reason: {reason}. You will be unmuted in {mins} minute(s).")

			db.execute("UPDATE users SET Warnings = Warnings + 1 WHERE UserName = ?",
				target)

		else:
			bot.send_message(f"/ban {target} Repeated infractions.")
			bot.send_message(f"{target}, you have been banned from chat for repeated infractions.")


def remove_warn(bot, user, target=None, *args):
	if target is None:
		bot.send_message("You must specify a target.")

	else:
		warnings = db.field("SELECT Warnings FROM users WHERE UserName = ?",
			target.lower())

		if warnings == 0:
			bot.send_message(f"{target} has not received any warnings.")

		else:
			db.execute("UPDATE users SET Warnings = Warnings - 1 WHERE UserName = ?",
				target)

			bot.send_message(f"Warning for {target} revoked.")