from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import Updater, InlineQueryHandler, ConversationHandler,CommandHandler, MessageHandler, Filters
from googletrans import Translator
import requests
import apiai
import json
import re

TOKEN = '1016477578:AAGmmknBxRKyIbh_2XmRhcuK-fXwW0wJ9JE'
DIALOG_TOKEN = '02ab3a2fe7494e2c80d38726ebeec2b0'
updater = Updater(token=TOKEN, use_context=True)
dp = updater.dispatcher

LANGUAGE, MODE = range(2)

def start(update, context):
    reply_keyboard = [['Japanese']]
    update.message.reply_text(
            'Hi! This is Daddy Danny, your best friend and go-to AI for learning Japanese with!'
            + ' Click to begin your journey to mastering 日本語 today. Daddy cannot wait'
            + ' (✿ ◕‿◕)',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return LANGUAGE


def selectMode(update, context):
    reply_keyboard = [['Alphabet', 'Vocabulary', 'Chat', 'Exit']]
    update.message.reply_text(
            '°。+ *´¨What do you want to do today?°。+ *´¨',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return MODE

def generateAlphabet(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=' ひらがな')

dp.add_handler(CommandHandler('alphabet', generateAlphabet))

def generateVocabulary(update, context): 
    context.bot.send_message(chat_id=update.message.chat_id, text='laze sia')

dp.add_handler(CommandHandler('vocabulary', generateVocabulary))

def translateJapaneseToEnglish(text):
    translator = Translator()
    translator.translate(text, dest='en', src='auto')
    return text

def receiveMessage(update, context):
    request = apiai.ApiAI(DIALOG_TOKEN).text_request()
    request.lang = 'auto'
    request.session_id = 'Small-Talk'
    request.query = update.message.text
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech'] # Take JSON answer, response is a string?    
    if response:
        response = translateJapaneseToEnglish(response)
        context.bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text='I dont understand!')

dp.add_handler(MessageHandler(Filters.text, receiveMessage))

def exit():
    update.message.reply_text('((o(;△;)o)) Nuuu you have to go? Daddy is sad...COME BACK SOON Ó╭╮Ò')
    return ConversationHandler.END

def main():
    conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', start)],
            states={
                LANGUAGE: [MessageHandler(Filters.regex('^(Japanese)$'), selectMode)],
                MODE: [MessageHandler(Filters.regex('^(Alphabet|Vocabulary|Chat|Exit)$'), start)]
                },
            fallbacks=[CommandHandler('exit', exit)]
            )
    dp.add_handler(conv_handler)
    updater.start_polling(clean=True)
    updater.idle()

if __name__ == '__main__':
    main()
