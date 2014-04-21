#!/usr/bin/env python
import os
import logging
import time
import irc, irc.bot

import websocket

from ChatExchange.SEChatWrapper import SEChatWrapper


logging.basicConfig(level=logging.DEBUG)

IRC_SERVER = 'cs1692x.moocforums.org'
IRC_PORT = 6667
IRC_CHANNEL = '#CS_CS169.1x'
IRC_NICK = 'STACKEXCHANGE'

SE_HOST = 'SO'
SE_ROOM_ID = 51078


class Bot(irc.bot.SingleServerIRCBot):
    def __init__(self):
        irc.bot.SingleServerIRCBot.__init__(
            self, [(IRC_SERVER, IRC_PORT)], IRC_NICK, IRC_NICK)

        self.se = SEChatWrapper(SE_HOST)
        self.se.login(
            os.environ['SE_CHAT_USERNAME'],
            os.environ['SE_CHAT_PASSWORD'],
        )
        self.se.joinRoom(SE_ROOM_ID)
        self.se.watchRoom(SE_ROOM_ID, self.on_se_message, 5)

    def on_se_message(self, message, chat):
        print chat
        self.connection.notice(IRC_CHANNEL,
            "%s: %s" % (
                message['user_name'], message['content']
            )
        )


    def on_welcome(self, c, event):
        c.join(IRC_CHANNEL)

    def on_pubmsg(self, connection, event):
        if IRC_NICK not in event.source.nick:
            body = event.arguments[0]
            self.se.sendMessage(SE_ROOM_ID, 
                "**%s (IRC):** %s" % (event.source.nick, body,))

Bot().start()