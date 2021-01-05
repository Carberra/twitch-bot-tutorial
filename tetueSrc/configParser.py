#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from configparser import ConfigParser

PATH_TO_CONFIG_FILE = 'files/login_data.cfg'

def get_configuration(section):
    dict_config = {}
    if os.path.isfile(PATH_TO_CONFIG_FILE):
        config = ConfigParser()
        config.read(PATH_TO_CONFIG_FILE)
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
        print("File or directory not exist, adapt configParser.PATH_TO_CONFIG_FILE")
        return False, dict_config

def main():
    read_successful, cfg = get_configuration("bot")
    print("Erfolgreich: " + str(read_successful) + " / " + str(cfg))

if __name__ == "__main__":
    main()