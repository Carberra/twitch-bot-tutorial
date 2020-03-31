from time import time

from . import misc, economy, games, mod

PREFIX = "!"


class Cmd(object):
	def __init__(self, callables, func, cooldown=0):
		self.callables = callables
		self.func = func
		self.cooldown = cooldown
		self.next_use = time()


# cmds = {
# 	"hello": misc.hello,
# }

cmds = [
	#	misc
	Cmd(["hello", "hi", "hey"], misc.hello, cooldown=15),
	Cmd(["about"], misc.about),
	Cmd(["uptime"], misc.uptime),
	Cmd(["userinfo", "ui"], misc.userinfo),
	Cmd(["shutdown"], misc.shutdown),

	#	economy
	Cmd(["coins", "money"], economy.coins),

	#	games
	Cmd(["coinflip", "flip"], games.coinflip, cooldown=300),
	Cmd(["heist"], games.start_heist, cooldown=60),

	#	mod
	Cmd(["warn"], mod.warn),
	Cmd(["unwarn", "rmwarn"], mod.remove_warn)
]


def process(bot, user, message):
	if message.startswith(PREFIX):
		cmd = message.split(" ")[0][len(PREFIX):]
		args = message.split(" ")[1:]
		perform(bot, user, cmd, *args)


def perform(bot, user, call, *args):
	if call in ("help", "commands", "cmds"):
		misc.help(bot, PREFIX, cmds)

	else:
		for cmd in cmds:
			if call in cmd.callables:
				if time() > cmd.next_use:
					cmd.func(bot, user, *args)
					cmd.next_use = time() + cmd.cooldown

				else:
					bot.send_message(f"Cooldown still in effect. Try again in {cmd.next_use-time():,.0f} seconds.")

				return

		bot.send_message(f"{user['name']}, \"{call}\" isn't a registered command.")