import db

def coins(bot, user, *args):
    coins = db.field("SELECT Coins FROM users WHERE UserID = ?", user.id)
    bot.send_message(f"{user.get_displayname()}, du besitzt {coins:,} coins.")

def statistics(bot, user, *args):
    userlist = db.records("SELECT UserID, MessagesSent, CountLogins, row_number() OVER(ORDER BY Warnings ASC, CountLogins DESC, LoyaltyPoints DESC, Coins DESC) as NoId FROM users")
    max_rows = db.field("SELECT Count(*) FROM users")
    for element in userlist:
        if element[0] == user.id:
            bot.send_message(f"@{user.get_displayname()}, dein aktueller Rang mit {element[2]} Logins und {element[1]} Nachrichten ist {element[3]}/{max_rows}.")
            break
