#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# COPYRIGHT INFORMATION
# ---------------------
# This bot is forked from Carberra YouTube channel: https://www.youtube.com/playlist?list=PLYeOw6sTSy6ZFDkfO9Kl8d37H_3wLyNxO
# This bot can be freely copied and modified without permission, but not sold as is.
# Some code in this file is licensed under the Apache License, Version 2.0.
# http://aws.amazon.com/apache2.0/

import sys
from irc.bot import SingleServerIRCBot
from requests import get
import tetueSrc
import user_management, db, react, automod, cmds

read_successful, cfg = tetueSrc.get_configuration("bot")

class Bot(SingleServerIRCBot):
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
        db.build()
        print("Online")
        self.send_message("Now online.")

    @db.with_commit
    def on_pubmsg(self, cxn, event):
        tags = {kvpair["key"]: kvpair["value"] for kvpair in event.tags}
        message = event.arguments[0]
        print(tags)
        active_user = user_management.get_active_user(tags["user-id"], tags["display-name"], tags["badges"])
        print(active_user.badge)
        if active_user.get_name() != cfg["name"] and automod.clear(bot, active_user, message):
            # Feature: Wenn man nur mal kurz sagen will, dass man da ist aber wieder im Lurch geht:  !Lurk Hallo an alle, lass mal en bissel Liebe da
            react.process(bot, active_user, message)
            cmds.process(bot, active_user, message)

    def send_message(self, message):
        self.connection.privmsg(self.CHANNEL, message)

if __name__ == "__main__":
    bot = Bot()
    bot.start()