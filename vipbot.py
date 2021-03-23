#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# COPYRIGHT INFORMATION
# ---------------------
# This bot is forked from Carberra YouTube channel: https://www.youtube.com/playlist?list=PLYeOw6sTSy6ZFDkfO9Kl8d37H_3wLyNxO
# This bot can be freely copied and modified without permission, but not sold as is.
# Some code in this file is licensed under the Apache License, Version 2.0.
# http://aws.amazon.com/apache2.0/

import sys, time, threading
from irc.bot import SingleServerIRCBot
from requests import get
import tetueSrc
import db

read_successful, cfg = tetueSrc.get_configuration("vipbot")

class VipBot(SingleServerIRCBot):
    def __init__(self):
        self.HOST = "irc.chat.twitch.tv"
        self.PORT = 6667
        self.USERNAME = cfg["name"].lower()
        self.CLIENT_ID = cfg["client_id"]
        self.TOKEN = cfg["token"]
        owner = cfg["owner"]
        self.CHANNEL = f"#{owner}"

        url = f"https://api.twitch.tv/kraken/users?login={self.USERNAME}"
        headers = {"Client-ID": self.CLIENT_ID, "Accept": "application/vnd.twitchtv.v5+json"}
        resp = get(url, headers=headers).json()
        self.channel_id = resp["users"][0]["_id"]

        super().__init__([(self.HOST, self.PORT, f"oauth:{self.TOKEN}")], self.USERNAME, self.USERNAME)

    def on_welcome(self, cxn, event):
        for req in ("membership", "tags", "commands"):
            cxn.cap("REQ", f":twitch.tv/{req}")

        cxn.join(self.CHANNEL)
        vip_user = db.column("SELECT UserName FROM users WHERE Badges = ?", "AutoVIP")
        print("Alte VIPs: " + str(vip_user))
        for element in vip_user:
            self.send_message(f"/unvip {element}")
            db.execute("UPDATE users SET Badges = ? WHERE UserName = ?", "Tueftlie", element)
            time.sleep(0.5)
        vip_user = db.column("SELECT UserName FROM users WHERE Badges = ? ORDER BY Warnings ASC, CountLogins DESC, LoyaltyPoints DESC, Coins DESC LIMIT ?", "Tueftlie", tetueSrc.get_int_element("autovip", "max_avail_auto_vips"))

        for element in vip_user:
            self.send_message(f"/vip {element}")
            db.execute("UPDATE users SET Badges = ? WHERE UserName = ?", "AutoVIP", element)
            time.sleep(0.5)
        print("Neue VIPs: " + str(vip_user))
        db.commit()
        db.close()
        self.disconnect()
        print("Beendet")
        self.die()

    def send_message(self, message):
        self.connection.privmsg(self.CHANNEL, message)

if __name__ == "__main__":
    print("Start")
    vipbot = VipBot()
    vipbot.start()
