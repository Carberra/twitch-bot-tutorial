import db

def coins(bot, user, *args):
    coins = db.field("SELECT Coins FROM users WHERE UserID = ?", user.id)
    bot.send_message(f"{user.get_displayname()}, du besitzt {coins:,} coins.")