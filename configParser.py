#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from configparser import ConfigParser

PATH_TO_CONFIG_FILE = 'login_data.cfg'

def get_configuration(section):
    config = ConfigParser()
    config.read(PATH_TO_CONFIG_FILE)
    dict_config = {}
    if config.has_section(section):
        for element in config.items(section):
            dict_config[element[0]] = element[1]
    else:
        return False, dict_config

    if len(dict_config) != 0:
        return True, dict_config
    else:
        return False, dict_config

