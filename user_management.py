#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import db

class Chatuser:
    def __init__(self, id, name, badgets):
        self.id = id
        self.name = name
        self.badgets = badgets # ToDo: iSEVEN: Ja ohne "T" halt LUL
        self.set_status()
        self.messages = 0
        self.statusIsActive = False

#    def get_user_status(self):
        #Wenn sich jemand in den Lurch verabschiedet, wird der Status auf "Lurch" gesetzt und später begrüßt mit "Willkommen aus dem Lurch"

    def set_status(self):
        self.status = None
        if self.badgets is None: return
        if "moderator" in self.badgets:
            self.status = "moderator"
        elif "vip" in self.badgets:
            self.status = "vip"
        elif "broadcaster" in self.badgets:
            self.status = "broadcaster"
    
    def get_status(self):
        return self.status

    def get_id(self):
        return self.id

    # Name wie er im Chat angezeigt wird: Technik_Tueftler
    def get_displayname(self):
        return self.name

    # Name in Keinbuchstaben: technik_tueftler
    def get_name(self):
        return self.name.lower()

    def get_badgets(self):
        return self.badgets
        
    def get_mod_rights(self):
        if self.status == "moderator":
            return True
        else:
            return False
    # def count_loyalty_points(self):
    #     if self.loyalty_points < 3: # ToDo: Die Anzahl der max. Punkte in die config mit einbinden.
    #         self.loyalty_points += 1
    # def get_loyalty_points(self):
    #     return self.loyalty_points
    def count_message(self):
        self.messages += 1
    def get_messages(self):
        return self.messages
    def get_user_active_status(self):
        return self.statusIsActive
    def set_user_active_status(self, status):
        print("Setze User: " + str(status))
        self.statusIsActive = status

activeUserList = [] # Aktive User im Chat
userListToday = [] # User die während des Stream schon mal da waren, sich aber wieder abgemeldet haben bzw. in den Lurch gegangen sind

def get_active_user(user_id, display_name, badges):
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
            new_user = Chatuser(user_id, display_name, badges)
            set_user_active(new_user)
            add_user_db(new_user)
            return new_user
        else:
            # Hier brauche ich noch keine Informationen aus der DB, kann aber dann hinzugefügt werden über tubel[index] --> temp_user_db[0] für User-ID
            print("User war in der Datenbank")
            old_user = Chatuser(user_id, display_name, badges)
            set_user_active(old_user)
            return old_user

def set_user_active(user):
    """
    Setzt den User aktiv und fügt ihn in in die entsprechenden Listen hinzu.
    """
    user_found = False
    for element in userListToday:
        if element.get_id() == user.get_id():
            activeUserList.append(element)
            user_found = True
            break
    if user_found == False:
        activeUserList.append(user)
        userListToday.append(user)

def set_user_inactive(user_id):
    for element in activeUserList:
        if element.get_id() == user_id:
            activeUserList.remove(element)
            element.set_user_active_status(False)
            return

def get_user_with_id_from_list(list, user_id):
    '''Prüft, ob ein User in der Listen vorhanden ist und gibt ihn zurück'''
    user_found = False
    user = None
    for element in list:
        if element.get_id() == user_id:
            user_found = True
            user = element
            break
    return user_found, user

def is_user_id_active(user_id):
    user_found = False
    for element in activeUserList:
        if element.get_id() == user_id:
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
    db.execute("INSERT OR IGNORE INTO users (UserID, UserName) VALUES (?, ?)", user.get_id(), user.get_name())

def main():
    pass

if __name__ == "__main__":
    main()