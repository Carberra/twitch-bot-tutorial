#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from configparser import ConfigParser

PATH_TO_INIT_FILE = 'files/login_data.priv'
PATH_TO_FILE_CONFIG_FILE = 'files/conf.cfg'

def get_string_element(section, option):
    if not os.path.isfile(PATH_TO_FILE_CONFIG_FILE): return ""
    config = ConfigParser()
    config.read(PATH_TO_FILE_CONFIG_FILE, "UTF-8")
    if not config.has_section(section): return ""
    if not config.has_option(section, option): return ""
    return config.get(section, option)

def get_int_element(section, option):
    if not os.path.isfile(PATH_TO_FILE_CONFIG_FILE): return 0
    config = ConfigParser()
    config.read(PATH_TO_FILE_CONFIG_FILE)
    if not config.has_section(section): return 0
    if not config.has_option(section, option): return 0
    try:
        return config.getint(section, option)
    except Exception:
        return 0

def get_string_list(section, option):
    "Return a list with all elements from a option welche are seperate by a comma"
    dict_string = {} # ToDo: warum dict und nicht list?
    if not os.path.isfile(PATH_TO_FILE_CONFIG_FILE): return dict_string
    config = ConfigParser()
    config.read(PATH_TO_FILE_CONFIG_FILE)
    if not config.has_section(section): return dict_string
    if not config.has_option(section, option): return dict_string
    dict_string = config.get(section, option).split(",")
    return dict_string

def get_configuration(section):
    dict_config = {}
    if os.path.isfile(PATH_TO_INIT_FILE):
        config = ConfigParser()
        config.read(PATH_TO_INIT_FILE)
        if config.has_section(section):
            for element in config.items(section):
                dict_config[element[0]] = element[1]
        else:
            print("No section: " + str(section))
            return False, dict_config

        if len(dict_config) != 0:
            return True, dict_config
        else:
            print("Empty section")
            return False, dict_config
    else:
        print("File or directory not exist, adapt configParser.PATH_TO_INIT_FILE")
        return False, dict_config

def main():
    read_successful, cfg = get_configuration("bot")
    print("Erfolgreich: " + str(read_successful) + " / " + str(cfg))
    print(get_string_list("automod", "badwords"))
    print(get_string_list("automod", "filler_sign"))

if __name__ == "__main__":
    main()