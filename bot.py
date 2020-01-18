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

def start(update, context):
    reply_keyboard = [['/japanese']]
    update.message.reply_text(
            'Hi! This is Daddy Danny, your best friend and go-to AI for learning languages!'
            + ' Please select which language you want to learn (✿ ◕‿◕)',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

start_handler = CommandHandler('start', start)
dp.add_handler(start_handler)

def selectMode(update, context):
    reply_keyboard = [['/alphabet', '/vocabulary', '/chat', '/exit']]
    update.message.reply_text(
            '°。*´¨What do you want to do today?° *´¨',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

mode_handler = CommandHandler('japanese', selectMode)
dp.add_handler(mode_handler)

def generateAlphabet(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=' ひらがな')

dp.add_handler(CommandHandler('alphabet', generateAlphabet))

def generateVocabulary(update, context): 
    context.bot.send_message(chat_id=update.message.chat_id, text='laze sia')

dp.add_handler(CommandHandler('vocabulary', generateVocabulary))

def translateJapaneseToEnglish(text):
    translator = Translator()
    translation = translator.translate(text, dest='en', src='ja')
    #print(translation.text)
    return translation.text

def translateEnglishToJapanese(text):
    translator = Translator()  # initalize the Translator object
    translation = translator.translate(text, dest='ja', src='en')  # translate two phrases to Hindi
    #print(translation.text)  
    return translation.text

def chat(update, context):
    request = apiai.ApiAI(DIALOG_TOKEN).text_request()
    request.lang = 'en'
    request.session_id = 'Small-Talk'
    raw_message = update.message.text
    message_en = translateJapaneseToEnglish(raw_message)
    request.query = message_en # Send request to AI with user message
    responseJson = json.loads(request.getresponse().read().decode('utf-8')) # response from server
    response = responseJson['result']['fulfillment']['speech'] # Take JSON answer, response is a string?    
    if response:
        response_ja = translateEnglishToJapanese(response)
        context.bot.send_message(chat_id=update.message.chat_id, text=response_ja)
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text='くそ! パパ・ダニーはばかです...ご不便をお許しください o(╥﹏╥)o')

dp.add_handler(MessageHandler(Filters.text, chat))

def chat(update, context):
    context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)

dp.add_handler(CommandHandler('chat', chat))

def exit(update, context):
    reply_keyboard = [['/start']]
    update.message.reply_text('((o(;△;)o)) Nuuu you have to go? Daddy is sad...COME BACK SOON Ó╭╮Ò', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    threading.Thread(target=shutdown).start()

exit_handler = CommandHandler('exit', exit)
dp.add_handler(exit_handler)

def main():
    updater.start_polling(clean=True)
    updater.idle()

if __name__ == '__main__':
    main()
