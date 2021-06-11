#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# COPYRIGHT INFORMATION
# ---------------------
# This bot is forked from Carberra YouTube channel: https://www.youtube.com/playlist?list=PLYeOw6sTSy6ZFDkfO9Kl8d37H_3wLyNxO
# This bot can be freely copied and modified without permission, but not sold as is.
# Some code in this file is licensed under the Apache License, Version 2.0.
# http://aws.amazon.com/apache2.0/

from irc.bot import SingleServerIRCBot
from requests import get
import tetueSrc
import user_management, db, react, automod, cmds

read_successful, cfg = tetueSrc.get_configuration("bot")
read_successful, cfg_owner = tetueSrc.get_configuration("vipbot")


class Bot(SingleServerIRCBot):
    def __init__(self):
        # Init for Chat-Bot
        self.HOST = "irc.chat.twitch.tv"
        self.PORT = 6667
        self.USERNAME = cfg["name"].lower()
        self.CLIENT_ID = cfg["client_id"]
        self.TOKEN = cfg["token"]
        self.owner = cfg["owner"]
        self.CHANNEL = f"#{self.owner}"
        url = f"https://api.twitch.tv/kraken/users?login={self.USERNAME}"
        headers = {"Client-ID": self.CLIENT_ID, "Accept": "application/vnd.twitchtv.v5+json"}
        resp = get(url, headers=headers).json()
        self.channel_id = resp["users"][0]["_id"]
        super().__init__([(self.HOST, self.PORT, f"oauth:{self.TOKEN}")], self.USERNAME, self.USERNAME)

        # Init for TeTue-Channel
        url_owner = f"https://api.twitch.tv/kraken/users?login={self.owner}"
        headers_owner = {"Client-ID": cfg_owner["client_id"], "Accept": "application/vnd.twitchtv.v5+json"}
        resp_owner = get(url_owner, headers=headers_owner).json()
        self.channel_id = resp_owner["users"][0]["_id"]

    def on_welcome(self, cxn, event):
        for req in ("membership", "tags", "commands"):
            cxn.cap("REQ", f":twitch.tv/{req}")

        cxn.join(self.CHANNEL)
        print("Chatroom joined")
        db.build()
        react.create_hen_name_list()
        print("Create Hennamelist")
        user_management.update_user_awards()
        print("Update awards")
        react.update_KD_Counter(bot)
        print("Update counter")
        tetueSrc.log_header_info("Stream-Start")
        self.send_message("En Gude Tüftlies " + tetueSrc.get_string_element("hunname", "icon"))
        print("Online")


    @db.with_commit
    def on_pubmsg(self, cxn, event):
        tags = {kvpair["key"]: kvpair["value"] for kvpair in event.tags}
        message = event.arguments[0]
        #print(event)
        tetueSrc.log_event_info(tags)
        tetueSrc.log_event_info(message)

        active_user = user_management.get_active_user(tags["user-id"], tags["display-name"], tags["badges"])
        if active_user.get_name() != cfg["name"] and automod.clear(bot, active_user, message):
            # Feature: Wenn man nur mal kurz sagen will, dass man da ist aber wieder im Lurch geht:  !Lurk Hallo an alle, lass mal en bissel Liebe da
            react.process(bot, active_user, message)
            cmds.process(bot, active_user, message)
            if "custom-reward-id" in tags:
                react.channel_point(bot, active_user, message, tags["custom-reward-id"])
            elif "bits" in tags:
                react.update_bits_records(bot, active_user, tags["bits"])
                react.thank_for_cheer(bot, active_user, tags["bits"])

    def send_message(self, message):
        self.connection.privmsg(self.CHANNEL, message)
    
    def get_channel_info(self):
        url = f"https://api.twitch.tv/kraken/channels/{self.channel_id}"
        headers = {"Client-ID": cfg_owner["client_id"], "Accept": "application/vnd.twitchtv.v5+json"}
        resp = get(url, headers=headers).json()
        stream_info = {"Game":None}
        try:
            stream_info["Game"] = resp["game"]
            if stream_info["Game"] != None:
                db.execute("INSERT OR IGNORE INTO category (Category, Wins, Loses) VALUES (?, ?, ?)", stream_info["Game"], 0, 0)
        except Exception:
            pass
        finally:
            return stream_info

    def get_chatroom_info(self):
        # {'_links': {}, 'chatter_count': 5, 'chatters': {'broadcaster': ['technik_tueftler'], 'vips': [], 'moderators': [], 'staff': [], 'admins': [], 'global_mods': [], 'viewers': ['carbob14xyz', 'dialogiktv', 'kopfsalto1337', 'streamelements']}}
        url = f"https://tmi.twitch.tv/group/user/{self.owner}/chatters"
        resp = get(url).json()
        return resp

    def get_extern_channel_info(self, user):
        url = f"https://api.twitch.tv/kraken/users?login={user}"
        headers = {"Client-ID": self.CLIENT_ID, "Accept": "application/vnd.twitchtv.v5+json"}
        return get(url, headers=headers).json()


if __name__ == "__main__":
    bot = Bot()
    bot.start()