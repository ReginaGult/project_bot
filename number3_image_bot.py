import telebot
from telebot import types
import pictures_config as config
import dbworker
import numpy as np
#import cv2
import os
#from IPython.display import display, Image
#import matplotlib.pyplot as plt
#import matplotlib.image as mpimg

import requests

bot = telebot.TeleBot(config.token)
path=os.getcwd()


@bot.message_handler(commands=["start"], content_types=['text'])
def cmd_start(message):
    state = dbworker.get_current_state(message.chat.id)
    if state == config.States.S_ENTER_NAME.value:
        bot.send_message(message.chat.id, "Хотел со мной познакомиться, давай =)")
    elif state == config.States.S_SEND_PIC.value:
        bot.send_message(message.chat.id, "Хочешь поделиться картинкой, я жду!")
    else: 
        bot.send_message(message.chat.id, "Привет! Как я могу к тебе обращаться?")
        dbworker.set_state(message.chat.id, config.States.S_ENTER_NAME.value)




@bot.message_handler(commands=["reset"])
def cmd_reset(message):
    bot.send_message(message.chat.id, "Опять? Ну и как тебя зовут?")
    dbworker.set_state(message.chat.id, config.States.S_ENTER_NAME.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_NAME.value)
def user_entering_name(message):
    bot.send_message(message.chat.id, "Очень приятно! Загружай картинку!")
    dbworker.set_state(message.chat.id, config.States.S_SEND_PIC.value)



    
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_SEND_PIC.value, content_types=['photo'])
def user_picture(message):
    bot.send_message(message.chat.id, "Успешно! Я жду еще картинку!")
    print ('message.photo =', message.photo)
    fileID = message.photo[-1].file_id
    print ('fileID =', fileID)
    file = bot.get_file(fileID)
    print ('file.file_path =', file.file_path)
    telegram_api='http://api.telegram.org/file/bot607054617:AAGQqyok0jvt1lKvpSqCjvTP7_f6C21RENA/photos/'
    long_url=os.path.join(telegram_api, file.file_path.rsplit('/',1)[-1])
    print(long_url)
    #image = urllib.URLopener()
    #image.retrieve(long_url,"00000001.jpg")
    with open(file.file_path.rsplit('/', 1)[-1], 'wb') as handle:
        response = requests.get(long_url, stream=True)

        if not response.ok:
            print (response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)

    
    

    #plt.imshow(mpimg.imread(long_url))
    #display(Image(filename=long_url))
  
    #cv2.imwrite(os.path.join(path , 'waka.jpg'), message)
    #cv2.waitKey(0)

    dbworker.set_state(message.chat.id, config.States.S_SEND_PIC.value)

"""
@bot.inline_handler(lambda query: len(query.query) > 0)
def query_text(query):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text="Нажми меня", callback_data="test"))
    results = []
    single_msg = types.InlineQueryResultArticle(
        id="1", title="Press me",
        input_message_content=types.InputTextMessageContent(message_text="Я – сообщение из инлайн-режима"),
        reply_markup=kb
    )
    results.append(single_msg)
    bot.answer_inline_query(query.id, results)
"""

if __name__ == '__main__':
    bot.polling(none_stop=True)  