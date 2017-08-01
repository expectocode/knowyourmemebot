#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic inline bot example. Applies different text transformations.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
from uuid import uuid4

import re
import configparser

from telegram import InlineQueryResultArticle, ParseMode, \
    InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import logging

import requests
from bs4 import BeautifulSoup
HEADERS = {'User-Agent':'Mozilla/5.0'}

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text('Hi! I am an inline bot, you should type my username and a search query.')

def help(bot, update):
    update.message.reply_text('Help!')

def escape_markdown(text):
    """Helper function to escape telegram markup symbols"""
    escape_chars = '\*_`\['
    return re.sub(r'([%s])' % escape_chars, r'\\\1', text)

def inlinequery(bot, update):
    query = update.inline_query.query
    if query != "":

        r = requests.get('http://knowyourmeme.com/search?q='+query.replace(' ','+'),headers=HEADERS)
        logger.debug(r)
        soup = BeautifulSoup(r.text)
        restabl = soup.find('table',{'class':'entry_list'})
        results = list()

        if restabl == None:
            results = [InlineQueryResultArticle(id=uuid4(),title='No Results',
                    input_message_content=InputTextMessageContent(query +': no results'))]
        else:
            if len(restabl.contents) >= 3:
                logger.debug('entry 1')
                entry1 = restabl.contents[1].contents[1]
                entry1url = 'http://knowyourmeme.com' + entry1.a['href']
                results.append(InlineQueryResultArticle(id=uuid4(),
                                                title=entry1.img['title'],
                                                thumb_url=entry1.img['data-src'],
                                                url=entry1url,
                                                hide_url=False,
                                                input_message_content=InputTextMessageContent(
                                                    '*{}*\n{}'.format(
                                                        entry1.img['title'],entry1url),
                                                    parse_mode=ParseMode.MARKDOWN
                                                )))
            if len(restabl.contents) >= 5:
                logger.debug('entry 2')
                entry2 = restabl.contents[1].contents[3]
                entry2url = 'http://knowyourmeme.com' + entry2.a['href']
                results.append(InlineQueryResultArticle(id=uuid4(),
                                                title=entry2.img['title'],
                                                thumb_url=entry2.img['data-src'],
                                                url=entry2url,
                                                hide_url=False,
                                                input_message_content=InputTextMessageContent(
                                                    '*{}*\n{}'.format(
                                                        entry2.img['title'],entry2url),
                                                    parse_mode=ParseMode.MARKDOWN
                                                    )))
            if len(restabl.contents) >= 7:
                logger.debug('entry 3')
                entry3 = restabl.contents[1].contents[5]
                entry3url = 'http://knowyourmeme.com' + entry3.a['href']
                results.append(InlineQueryResultArticle(id=uuid4(),
                                                title=entry3.img['title'],
                                                thumb_url=entry3.img['data-src'],
                                                url=entry3url,
                                                hide_url=False,
                                                input_message_content=InputTextMessageContent(
                                                    '*{}*\n{}'.format(
                                                        entry3.img['title'],entry3url),
                                                    parse_mode=ParseMode.MARKDOWN
                                                )))
            if len(restabl.contents) >= 9:
                logger.debug('entry 4')
                entry4 = restabl.contents[1].contents[7]
                entry4url = 'http://knowyourmeme.com' + entry3.a['href']
                results.append(InlineQueryResultArticle(id=uuid4(),
                                                title=entry4.img['title'],
                                                thumb_url=entry4.img['data-src'],
                                                url=entry4url,
                                                hide_url=False,
                                                input_message_content=InputTextMessageContent(
                                                    '*{}*\n{}'.format(
                                                        entry4.img['title'],entry4url),
                                                    parse_mode=ParseMode.MARKDOWN
                                                )))
    #        r = requests.get(entry1url,headers=HEADERS)
    #        logger.debug(r)
    #        soup = BeautifulSoup(r.text)
    #        met = soup.find('meta',{'name':'description'})

        bot.answer_inline_query(update.inline_query.id, results)
    #update.(results)

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    bot_token = config['config']['token']
    # Create the Updater and pass it your bot's token.
    updater = Updater(bot_token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", start))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(InlineQueryHandler(inlinequery))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
