#!/usr/bin/python

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.

import random
import telebot as t

API_TOKEN = '7053339260:AAE65e21v_tMhqlwHEb4AZqisDyr5pqFssY'

bot = t.TeleBot(API_TOKEN)

recipes = []


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, 'Hi there, I am EchoBot. I am here to echo your kind words back to you. Just say anything nice and I\'ll say the exact same thing to you!')


@bot.message_handler(regexp='#рецепт|#Рецепт|#recipe|#Recipe')
def echo_message(message):
    print(message.message_id)
    markup = t.types.InlineKeyboardMarkup()
    callback_data = f'save_recipe,{message.message_id}'
    save_btn = t.types.InlineKeyboardButton('Сохранить', callback_data=callback_data)
    markup.add(save_btn)
    bot.reply_to(message, 'Заебись рецепт! Сохранить?', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: callback.data.split(',')[0] == 'save_recipe')
def handle_save_recipe_query(callback):
    print('mama')
    message_id = callback.data.split(',')[1]
    print(message_id)
    recipes.append(message_id)


@bot.message_handler(commands=['random'])
def get_random_recipe(message):
    bot.forward_message(message.chat.id, message.chat.id, random.choice(recipes))


bot.infinity_polling()
