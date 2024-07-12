# Telegram Bot Name: FirstBot
# Telegram Bot Username: @First1010bot
# Make sure you have python 3.8+ to run this framework
# $ pip install python-telegram-bot --upgrade

import os
from dotenv import load_dotenv
load_dotenv()

import logging
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler, InlineQueryHandler

from uuid import uuid4

# This part is for setting up logging module, so you will know when (and why) things don't work as expected:
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    results = []
    results.append(InlineQueryResultArticle(id=str(uuid4()), title="Caps", input_message_content=InputTextMessageContent(query.upper())))
    
    await context.bot.answer_inline_query(update.inline_query.id, results)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE): # To handle unrecognise command should user enter something that we didn't declare
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv('BOT_TOKEN')).build()
    
    start_handler = CommandHandler('start', start) # add a command that you are listening for, and assign it to a function that executes upon receiving this command.
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo) # The filters module contains a number of so-called filters that filter incoming messages for text, images, status updates and more. Any message that returns True for at least one of the filters passed to MessageHandler will be accepted. 
    caps_handler = CommandHandler("caps", caps)
    inline_caps_handler = InlineQueryHandler(inline_caps)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    application.add_handler(start_handler) # add handler to the application bot
    application.add_handler(echo_handler)
    application.add_handler(caps_handler)
    application.add_handler(inline_caps_handler)
    application.add_handler(unknown_handler) # the unknown command handler must be added last because if one of the previous handler matches, then it will execute that and ignore the bottom lines.
    
    application.run_polling()