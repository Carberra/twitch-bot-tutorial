from .. import db


def coins(bot, user, *args):
	coins = db.field("SELECT Coins FROM users WHERE UserID = ?", user.get_id())
	bot.send_message(f"{user.get_displayname()}, you have {coins:,} coins.")