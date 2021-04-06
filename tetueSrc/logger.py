#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import tetueSrc

logging.basicConfig(
    handlers=[logging.FileHandler(tetueSrc.get_string_element("paths", "logfile"), 'a', 'utf-8')],
    format='[%(asctime)s] %(levelname)-10s %(message)s',
    level=logging.INFO
)

def log_event_info(message):
    logging.info(message)

def log_header_info(message):
    with open(tetueSrc.get_string_element("paths", "logfile"), "a", encoding="utf-8") as f:
        f.write(f'# {message}\n')

def main():
    pass

if __name__ == "__main__":
    main()