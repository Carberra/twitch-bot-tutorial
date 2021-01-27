from collections import defaultdict
import db

warning_timers = (1, 5, 60)
BAD_WORDS_LIST = ("bum", "poo", "depp", "d3pp")
FILLER_WORDS = (" ", ".", "!")

def clear(bot, user, message):
    if any([word in message.lower() for word in BAD_WORDS_LIST]):
        warn(bot, user)
        return False
    return True

def warn(bot, user):
    warnings = db.field("SELECT Warnings FROM users WHERE UserID = ?", user.get_id())
    if warnings < len(warning_timers):
        mins = warning_timers[warnings]
        bot.send_message(f"/timeout {user.get_displayname()} {mins}m")
        bot.send_message(f"{user.get_displayname()}, du hast einen Timeout bekommen, weil du gegen die Chatregeln verstoßen hast. Die Timeoutlänge beträgt {mins} Minute(n).")

        db.execute("UPDATE users SET Warnings = Warnings + 1 WHERE UserID = ?", user.get_id())

    else:
        bot.send_message(f"/ban {user.get_displayname()} Repeated infractions.")
        bot.send_message(f"{user.get_displayname()}, you have been banned from chat for repeated infractions.")

def testbla(para1, para2, para3=None):
    print(para1)
    print(para2)
    print(para3)

def main():
    testbla("Zeile 1", "Zeile 2")
    testbla("Zeile 1", "Zeile 2", para3="Zeile 3")
    text = "halLO du d.e.p p"
    temp_text = text.lower()
    for element in FILLER_WORDS:
        temp_text = temp_text.replace(element, "")
        
    # for zeichen in BAD_WORDS_LIST:
    #     if zeichen in temp_text:
    #         print("gefunden: " + zeichen)
    #         break

    # if any(element in temp_text for element in BAD_WORDS_LIST):
    #     print(element)
    if any(word in temp_text for word in BAD_WORDS_LIST):
        print("Böses Wort gefunden")

    temp_text2 = "hallo du depp"
    said_badwords = [word for word in temp_text2.lower().split() if word in BAD_WORDS_LIST]
    print(said_badwords)

if __name__ == "__main__":
    main()