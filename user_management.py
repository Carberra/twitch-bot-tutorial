#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import db, tetueSrc
from enum import Enum, auto
from random import choice

user_awards = {}

class Badge(Enum):
    Broadcaster = auto()
    Moderator = auto()
    #Gruender = auto()
    ManuVIP = auto()
    AutoVIP = auto()
    Tueftlie = auto()
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value

def abstract_badge(badge_from_string):
    """
    Diese Funktion prüft den tag aus der Chatnachricht und ordnet ein badge aus dem user_management zu.
    Auch wird das badge aus der Datenbank geprüft und der Klasse Badge zugeordnet
    Beispiel: "broadcaster/1,subscriber/0,premium/1" --> Broadcaster
    """
    if badge_from_string is None: return Badge.Tueftlie
    if "moderator" in badge_from_string: return Badge.Moderator
    if "Broadcaster" in badge_from_string: return Badge.Broadcaster
    if "Moderator" in badge_from_string: return Badge.Moderator
    if "ManuVIP" in badge_from_string: return Badge.ManuVIP
    if "AutoVIP" in badge_from_string: return Badge.AutoVIP
    if "Tueftlie" in badge_from_string: return Badge.Tueftlie
    return Badge.Tueftlie

    # ToDo: Gründerabzeichen einfügen, richtig sortieren und alle badges der chatter einfügen

class Chatuser:
    def __init__(self, id, name, badge, hunname):
        self.id = id
        self.name = name
        self.badge = badge
        self.messages = 0
        self.statusIsActive = False
        self.hunname = hunname
        self.failedCmd = 0
        self.user_award = get_user_award(self.id)
        self.displaynames = [name for name in [self.name, self.hunname, self.user_award] if (name != None)]

    def user_welcome(self):
        if not self.hunname:
            return self.name
        else:
            return self.hunname

    # Name wie er im Chat angezeigt wird: Technik_Tueftler
    def get_displayname(self):
        return choice(self.displaynames)

    # Name in Keinbuchstaben: technik_tueftler
    def get_name(self):
        return self.name.lower()
    def get_mod_rights(self): # ToDo: badge direkt abfragen im code, kein getter
        if self.badge == Badge.Moderator:
            return True
        else:
            return False
    def count_message(self):
        self.messages += 1
    def __eq__(self, other):
        return self.id == other.id


activeUserList = [] # Aktive User im Chat
userListToday = [] # User die während des Stream schon mal da waren, sich aber wieder abgemeldet haben bzw. in den Lurch gegangen sind


def update_user_awards():
    global user_awards
    liste_award_db = ["Tueftelhuhn", "Kampfhuhn", "Sporthuhn", "MessagesSent", "Wasserhuhn"]
    liste_award_spell = ["Tüftelhuhn", "Kampfhuhn", "Sporthuhn", "Quatschhuhn", "Feuerwehrhuhn"]
    liste_id = []

    query_award_start = "SELECT UserID FROM awards "
    query_users_start = "SELECT UserID FROM users "
    query_order = "ORDER BY %s DESC"
    query_where = "WHERE (UserID IS NOT %s) "
    query_where_and = "AND (UserID IS NOT %s)"

    # Index 0
    query = query_award_start + query_order
    liste_id.append(db.field(query % (liste_award_db[0])))
    # Index 1
    query = query_award_start + query_where + query_order
    liste_id.append(db.field(query % (liste_id[0], liste_award_db[1])))
    # Index 2
    query = query_award_start + query_where + query_where_and + query_order
    liste_id.append(db.field(query % (liste_id[0], liste_id[1], liste_award_db[2])))
    # Index 3
    query = query_users_start + query_where + query_where_and + query_where_and + query_order
    liste_id.append(db.field(query % (liste_id[0], liste_id[1], liste_id[2], liste_award_db[3])))
    # Index 4
    query = query_award_start + query_where + query_where_and + query_where_and + query_where_and + query_order
    liste_id.append(db.field(query % (liste_id[0], liste_id[1], liste_id[2], liste_id[3], liste_award_db[4])))

    for index in range(len(liste_award_db)):
        user_awards[liste_award_spell[index]] = liste_id[index]


def get_user_award(user_id):
    award = None
    for key, val in user_awards.items():
        if user_id == val:
            award = key
            break
    return award


def get_active_user(user_id, display_name, badge):
    """
    Diese Funktion prüft, ob der User schon in einer der Listen ist und gibt das Objekt zurück.
    Weiterhin wird der Status des Users angepasst. Sollte der User nicht existieren, wird er 
    in der Datenbank erstellt.
    """
    user_active_found, user = get_user_with_id_from_list(activeUserList, user_id)
    if user_active_found == True: return user
    user_active_found, user = get_user_with_id_from_list(userListToday, user_id)
    if user_active_found == True:
        set_user_active(user)
        return user
    else:
        user_db = db.record("SELECT * FROM users WHERE UserID = ?", user_id)
        if user_db == None: # Check if user not in DB
            new_user = Chatuser(user_id, display_name, abstract_badge(badge), "")
            set_user_active(new_user)
            add_user_db(new_user)
            return new_user
        else:
            # Hier brauche ich noch keine Informationen aus der DB, kann aber dann hinzugefügt werden über tubel[index] --> temp_user_db[0] für User-ID
            #print("User war in der Datenbank")
            old_user = Chatuser(user_id, display_name, abstract_badge(user_db[10]), user_db[11])
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
            element.statusIsActive = False
            return

def remove_user_from_active_list(user_id):
    for element in activeUserList[:]:
        if element.id == user_id:
            activeUserList.remove(element)
            userListToday.remove(element)
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

#def get_user_with_name_from_list():

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
    # --------------- Hen-Name ---------------
    # import timeit
    # start = timeit.default_timer()
    # namelist = tetueSrc.get_string_list("hunname","name")
    # proplist = tetueSrc.get_string_list("hunname","propertie")
    # hennamelist = db.column("SELECT HenName FROM users WHERE HenName IS NOT NULL")

    # print(hennamelist)
    # num = 0
    # hen_name_list = []
    # for name in namelist:
    #     for prop in proplist:
    #         if name.lower().startswith(prop[:1]):
    #             henname = prop + str(" ") + name
    #             if henname not in hennamelist:
    #                 hen_name_list.append(henname)
    # print(num)
    # stop = timeit.default_timer()
    # print('Time: ', stop - start)
    # start = timeit.default_timer()
    # # expression for name in list_1 for element in list_2 if condition
    # list_3 = [("".join([prop, " ", name])) for name in namelist for prop in proplist if (name.lower().startswith(prop[:1])and("".join([prop, " ", name]) not in hennamelist))]
    # print(len(list_3))
    # print(choice(list_3))
    # stop = timeit.default_timer()
    # print('Time: ', stop - start)
    # henname = choice([("".join([prop, " ", name])) for name in namelist for prop in proplist if (name.lower().startswith(prop[:1])and("".join([prop, " ", name]) not in hennamelist))])
    # print(henname)
#    user = Chatuser(555, "test", Badge.Tueftlie, "Huhn")
#    print(user.badge)
#    if Badge.Tueftlie.value == Badge.Broadcaster.value:
#        print("Jopa")
#    else:
#        print("nope")

    update_user_awards()
    print(user_awards)

if __name__ == "__main__":
    main()
