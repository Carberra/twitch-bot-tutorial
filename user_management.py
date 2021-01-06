#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Chatuser:
    def __init__(self, id, name, badgets):
        self.id = id
        self.name = name
        self.badgets = badgets
        self.set_status()
        self.messages = 0
        self.loyalty_points = 0
        self.statusIsActive = True

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
    def count_loyalty_points(self):
        if self.loyalty_points < 3: # ToDo: Die Anzahl der max. Punkte in die config mit einbinden.
            self.loyalty_points += 1
    def get_loyalty_points(self):
        return self.loyalty_points
    def count_message(self):
        self.messages += 1
    def get_messages(self):
        return self.messages

activeUserList = []
userListToday = []

def set_user_active(user):
    activeUserList.append(user)

def set_user_inactive(user_id):
    for element in activeUserList:
        if element.get_id() == user_id:
            activeUserList.remove(element)
            return

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

def main():
    pass

if __name__ == "__main__":
    main()