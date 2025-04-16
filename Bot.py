import telebot
from telebot import types

import json

print('loading settings')
settings = json.load(open('config.json', 'r'))



import g4f
from g4f.client import Client


client = Client()

def answerpls(message):


    response = client.chat.completions.create(
        model=settings["model"],
        provider=settings["provider"],
        messages=[{"role": "system", "content": settings["prompt"]},
            {
                "role": "user",
                "content": message
            }
        ],
        stream=False,
        web_search = True
    )

    return response.choices[0].message.content
    


trustedusers = settings['trustedUsers']



print(trustedusers)
print('loaded')

def trust(func):
    def innerq(*args, **kwargs):
        username = args[0].chat.username
        if username in trustedusers:
            func(*args, **kwargs)
        else:
            print('UNTRUSTED USER')
    return innerq



bot = telebot.TeleBot(settings['token'])


@bot.message_handler(commands=['start', 'help'])
@trust
def send_welcome(message):
    #print(message.chat.id)
    bot.reply_to(message, "Просто напишите сообщение, а бот отправит вам ответ от нейросети!")



@bot.message_handler()
@trust
def aimsg(message):
    bot.send_message(message.chat.id, "Ждем ответ нейросети...")
    answer = answerpls(message.text)
    bot.edit_message_text(answer, message.chat.id, message.message_id+1)





bot.infinity_polling()