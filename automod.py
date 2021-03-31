from collections import defaultdict
import db
import tetueSrc

warning_timers = (1, 5, 60)
filler_sign_list = tetueSrc.get_string_list("automod", "filler_sign")
bad_word_list = tetueSrc.get_string_list("automod", "badwords")
failed_cmd_thr = tetueSrc.get_int_element("automod", "failed_cmd_thr")

def clear(bot, user, message):
    temp_message = message.lower()
    for element in filler_sign_list:
        temp_message = temp_message.replace(element, "")
    if any(word in temp_message for word in bad_word_list):
        warn(bot, user)
        return False
    return True

def check_spam_cmd(bot, user):
    # Prüft ob der User den cmd Befehl als Spam benutzt. Wenn Anzahl überschritten, bekommt er ein
    # Timeout aber keine Verwarnung eingetragen.
    user.failedCmd += 1
    if user.failedCmd >= failed_cmd_thr:
        bot.send_message(f"/timeout {user.get_displayname()} 1m")
        bot.send_message(f"{user.get_displayname()}, du hast einen Timeout bekommen, weil du zu häufig falsche Befehle eingegeben hast. Die Timeoutlänge beträgt 1 Minute.")
        return False
    else:
        return True

def warn(bot, user):
    warnings = db.field("SELECT Warnings FROM users WHERE UserID = ?", user.id)
    if warnings < len(warning_timers):
        mins = warning_timers[warnings]
        bot.send_message(f"/timeout {user.get_displayname()} {mins}m")
        bot.send_message(f"{user.get_displayname()}, du hast einen Timeout bekommen, weil du gegen die Chatregeln verstoßen hast. Die Timeoutlänge beträgt {mins} Minute(n).")

        db.execute("UPDATE users SET Warnings = Warnings + 1 WHERE UserID = ?", user.id)

    else:
        bot.send_message(f"/ban {user.get_displayname()} wiederholter Verstoß.")
        bot.send_message(f"{user.get_displayname()}, du wurdest wegen wiederholter Verstöße der Chatregeln aus dem Chat verbannt.")

def testbla(para1, para2, para3=None):
    print(para1)
    print(para2)
    print(para3)

def main():
    testbla("Zeile 1", "Zeile 2")
    testbla("Zeile 1", "Zeile 2", para3="Zeile 3")
    FILLER_WORDS = tetueSrc.get_string_list("automod", "filler_sign")
    BAD_WORDS_LIST = tetueSrc.get_string_list("automod", "badwords")
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