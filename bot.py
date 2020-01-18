from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters
import requests
import apiai
import json
import re

TOKEN = '1016477578:AAGmmknBxRKyIbh_2XmRhcuK-fXwW0wJ9JE'
DIALOG_TOKEN = '02ab3a2fe7494e2c80d38726ebeec2b0'
updater = Updater(token=TOKEN, use_context=True)
dp = updater.dispatcher

def get_url():
    contents = requests.get('https://random.dog/woof.json').json()    
    url = contents['url']
    return url

def get_image_url():
    allowed_extension = ['jpg','jpeg','png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url()
        file_extension = re.search("([^.]*)$",url).group(1).lower()
    return url

def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def bop(update, context):
    url = get_image_url()
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo=url)

def receiveMessage(update, context):
    request = apiai.ApiAI(DIALOG_TOKEN).text_request()
    request.lang = 'en'
    request.session_id = 'Small-Talk'
    request.query = update.message.text
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech'] # Take JSON answer
    if response:
        context.bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text='I dont understand!')

dp.add_handler(MessageHandler(Filters.text, receiveMessage))

def main():
    dp.add_handler(CommandHandler('bop',bop))
    updater.start_polling(clean=True)
    updater.idle()

if __name__ == '__main__':
    main()
