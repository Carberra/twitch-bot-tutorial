#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
from configparser import ConfigParser

PATH_TO_INIT_FILE = 'files/login_data.priv'
PATH_TO_FILE_CONFIG_FILE = 'files/config.json'

with open (PATH_TO_FILE_CONFIG_FILE, encoding='utf-8') as file:
    data = json.load(file)

def get_dict(section, option):
    if section not in data: return {}
    if option not in data[section]: return {}
    return data[section][option]

def get_string_element(section, option):
    if section not in data: return ""
    if option not in data[section]: return ""
    return str(data[section][option])

def get_int_element(section, option):
    if section not in data: return 0
    if option not in data[section]: return 0
    try:
        return int(data[section][option])
    except Exception:
        return 0

def get_string_list(section, option):
    if section not in data: return []
    if option not in data[section]: return []
    return data[section][option]

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
    print(get_string_list("automod", "list_badwords"))
    print(get_string_list("automod", "list_filler_sign"))

if __name__ == "__main__":
    main()