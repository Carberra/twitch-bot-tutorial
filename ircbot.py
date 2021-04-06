import logging
import sys
import tetueSrc

from irc.bot import SingleServerIRCBot

# config
HOST = 'irc.twitch.tv'
PORT = 6667
read_successful, cfg = tetueSrc.get_configuration("bot")
CLIENT_ID = cfg["client_id"]
owner = cfg["owner"]
USERNAME = cfg["name"].lower()
TOKEN = cfg["token"]
PASSWORD = f"oauth:{TOKEN}"
CHANNEL = f"#{owner}"

def _get_logger():
    logger_name = 'vbot'
    logger_level = logging.DEBUG
    log_line_format = '%(asctime)s | %(name)s - %(levelname)s : %(message)s'
    log_line_date_format = '%Y-%m-%dT%H:%M:%SZ'
    logger_ = logging.getLogger(logger_name)
    logger_.setLevel(logger_level)
    logging_handler = logging.StreamHandler(stream=sys.stdout)
    logging_handler.setLevel(logger_level)
    logging_formatter = logging.Formatter(log_line_format, datefmt=log_line_date_format)
    logging_handler.setFormatter(logging_formatter)
    logger_.addHandler(logging_handler)
    return logger_

logger = _get_logger()


class VBot(SingleServerIRCBot):

    VERSION = '1.0.0'

    def __init__(self, host, port, nickname, password, channel):
        logger.debug('VBot.__init__ (VERSION = %r)', self.VERSION)
        SingleServerIRCBot.__init__(self, [(host, port, password)], nickname, nickname)
        self.channel = channel
        self.viewers = []

    def on_welcome(self, connection, event):
        logger.debug('VBot.on_welcome')
        connection.join(self.channel)
        connection.privmsg(event.target, 'Hello world!')

    def on_join(self, connection, event):
        logger.debug('VBot.on_join')
        nickname = self._parse_nickname_from_twitch_user_id(event.source)
        self.viewers.append(nickname)

        if nickname.lower() == connection.get_nickname().lower():
            connection.privmsg(event.target, 'Hello world!')

    def on_part(self, connection, event):
        logger.debug('VBot.on_part')
        nickname = self._parse_nickname_from_twitch_user_id(event.source)
        self.viewers.remove(nickname)

    def on_pubmsg(self, connection, event):
        logger.debug('VBot.on_pubmsg')
        message = event.arguments[0]
        logger.debug('message = %r', message)
        message_parts = message.split(":", 1)
        if len(message_parts) > 1 and message_parts[0].lower() == connection.get_nickname().lower():
            self.do_command(event, message_parts[1].strip())

    def do_command(self, event, command):
        logger.debug('VBot.do_command (command = %r)', command)

        if command == "version":
            version_message = 'Version: %s' % self.VERSION
            self.connection.privmsg(event.target, version_message)
        if command == "count_viewers":
            num_viewers = len(self.viewers)
            num_viewers_message = 'Viewer count: %d' % num_viewers
            self.connection.privmsg(event.target, num_viewers_message)
        elif command == 'exit':
            self.die(msg="")
        else:
            logger.error('Unrecognized command: %r', command)

    @staticmethod
    def _parse_nickname_from_twitch_user_id(user_id):
        # nickname!username@nickname.tmi.twitch.tv
        return user_id.split('!', 1)[0]


def main():
    my_bot = VBot(HOST, PORT, USERNAME, PASSWORD, CHANNEL)
    my_bot.start()


if __name__ == '__main__':
    main()