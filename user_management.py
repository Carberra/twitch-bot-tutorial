#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import db
from enum import Enum, auto

class Badge(Enum):
    Broadcaster = auto()
    Moderator = auto()
    ManuVIP = auto()
    AutoVIP = auto()
    Knorzer = auto()

def abstract_badge(badge_from_string):
    """
    Diese Funktion prüft den tag aus der Chatnachricht und ordnet ein badge aus dem user_management zu.
    Auch wird das badge aus der Datenbank geprüft und der Klasse Badge zugeordnet
    Beispiel: "broadcaster/1,subscriber/0,premium/1" --> Broadcaster
    """
    if badge_from_string is None: return Badge.Knorzer
    if "moderator" in badge_from_string: return Badge.Moderator
    if "Broadcaster" in badge_from_string: return Badge.Broadcaster
    if "Moderator" in badge_from_string: return Badge.Moderator
    if "ManuVIP" in badge_from_string: return Badge.ManuVIP
    if "AutoVIP" in badge_from_string: return Badge.AutoVIP
    if "Knorzer" in badge_from_string: return Badge.Knorzer

class Chatuser:
    def __init__(self, id, name, badge):
        self.id = id
        self.name = name
        self.badge = badge
        self.messages = 0
        self.statusIsActive = False
    
    # Name wie er im Chat angezeigt wird: Technik_Tueftler
    def get_displayname(self):
        return self.name
    # Name in Keinbuchstaben: technik_tueftler
    def get_name(self):
        return self.name.lower()
    def get_mod_rights(self):
        if self.badge == Badge.Moderator:
            return True
        else:
            return False
    def count_message(self):
        self.messages += 1

activeUserList = [] # Aktive User im Chat
userListToday = [] # User die während des Stream schon mal da waren, sich aber wieder abgemeldet haben bzw. in den Lurch gegangen sind

def get_active_user(user_id, display_name, badge):
    """
    Diese Funktion prüft, ob der User schon in einer der Listen ist und gibt das Objekt zurück.
    Weiterhin wird der Status des Users angepasst. Sollte der User nicht existieren, wird er 
    in der Datenbank erstellt.
    """
    user_active_found, user = get_user_with_id_from_list(activeUserList, user_id)
    if user_active_found == True: return user
    print("User war nicht aktiv")
    user_active_found, user = get_user_with_id_from_list(userListToday, user_id)
    if user_active_found == True:
        print("User war inaktiv")
        set_user_active(user)
        return user
    else:
        print("User war nicht inaktiv")
        user_db = db.record("SELECT * FROM users WHERE UserID = ?", user_id)
        if user_db == None: # Check if user not in DB
            print("User war nicht in der Datenbank")
            new_user = Chatuser(user_id, display_name, abstract_badge(badge))
            set_user_active(new_user)
            add_user_db(new_user)
            return new_user
        else:
            # Hier brauche ich noch keine Informationen aus der DB, kann aber dann hinzugefügt werden über tubel[index] --> temp_user_db[0] für User-ID
            print("User war in der Datenbank")
            old_user = Chatuser(user_id, display_name, abstract_badge(user_db[10]))
            set_user_active(old_user)
            return old_user

def set_user_active(user):
    """
    Setzt den User aktiv und fügt ihn in in die entsprechenden Listen hinzu.
    """
    user_found = False
    for element in userListToday:
        if element.id == user.id:
            activeUserList.append(element)
            user_found = True
            break
    if user_found == False:
        activeUserList.append(user)
        userListToday.append(user)

def set_user_inactive(user_id):
    for element in activeUserList:
        if element.id == user_id:
            activeUserList.remove(element)
            element.statusIsActive  = False
            return

def get_user_with_id_from_list(list, user_id):
    '''Prüft, ob ein User in der Listen vorhanden ist und gibt ihn zurück'''
    user_found = False
    user = None
    for element in list:
        if element.id == user_id:
            user_found = True
            user = element
            break
    return user_found, user

def is_user_id_active(user_id):
    user_found = False
    for element in activeUserList:
        if element.id == user_id:
            user_found = True
            break
    return user_found

def is_user_name_active(user_name):
    user_found = False
    for element in activeUserList:
        if element.get_name() == user_name:
            user_found = True
            break
    return user_found

def add_user_db(user):
    db.execute("INSERT OR IGNORE INTO users (UserID, UserName) VALUES (?, ?)", user.id, user.get_name())

def main():
    # warnings = db.column("SELECT Warnings, Coins FROM users WHERE CountLogins = ?", 2)
    # warnings = db.column("SELECT UserName, CountLogins, LoyaltyPoints, Coins FROM users WHERE Badges = ? ORDER BY CountLogins DESC, LoyaltyPoints DESC, Coins DESC", "Knorzer")
    # warnings = db.column("SELECT Badges FROM users")
    # print(warnings)
    # print(type(warnings))
    temp_user = Chatuser(1234, "Roland", "broadcaster/1,subscriber/0,premium/1")
    print(temp_user.id)
    temp_user.id = 77
    print(temp_user.id)

if __name__ == "__main__":
    main()
