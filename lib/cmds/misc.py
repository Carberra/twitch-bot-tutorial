from datetime import timedelta
from sys import exit
from time import time

from .. import db

BOOT_TIME = time()
OWNER = "superbootwitch"


def help(bot, prefix, cmds):
	bot.send_message(f"Registered commands: "
		+ ", ".join([f"{prefix}{cmd.callables[0]}" for cmd in sorted(cmds, key=lambda cmd: cmd.callables[0])]))

	bot.send_message(f"Registered commands (incl. aliases): "
		+ ", ".join([f"{prefix}{'/'.join(cmd.callables)}" for cmd in sorted(cmds, key=lambda cmd: cmd.callables[0])]))


def about(bot, user ,*args):
	bot.send_message("Version 1.0.0. Developed by Carberra (Parafoxia).")


def hello(bot, user, *args):
	bot.send_message(f"Hey {user['name']}!")


def uptime(bot, user, *args):
	bot.send_message(f"The bot has been online for {timedelta(seconds=time()-BOOT_TIME)}.")


def userinfo(bot, user, *args):
	bot.send_message(f"Name: {user['name']}. ID: {user['id']}.")


def shutdown(bot, user, *args):
	if user["name"].lower() == OWNER:
		bot.send_message("Shutting down.")
		db.commit()
		db.close()
		bot.disconnect()
		exit(0)

	else:
		bot.send_message("You can't do that.")