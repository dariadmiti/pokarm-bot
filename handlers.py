#!/usr/bin/python

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.

from bot import bot
import telebot as t
from auth import message_auth

from sqlalchemy.orm import sessionmaker
from models import engine, Recipe

Session = sessionmaker(bind=engine)
session = Session()


telegram_session = {}


# users = session.query(User).all()
# for user in users:
#     print(f"ID: {user.id}, Name: {user.name}, Age: {user.age}, Email: {user.email}")


@bot.message_handler(commands=['help', 'start']) 
@message_auth
def send_welcome(message):
    bot.send_message(message.chat.id, 'Привет, мир!')


@bot.message_handler(commands=['add_recipe']) 
@message_auth
def ask_recipe_name(message):
    telegram_session[message.from_user.id] = {'add_recipe': {}}
    bot.send_message(message.chat.id, 'Отлично! Какое название?')

@bot.message_handler()
@message_auth
def handle_message(message):
    user_session = telegram_session[message.from_user.id]
    if 'add_recipe' in user_session:
        if 'name' not in user_session['add_recipe']:
            user_session['add_recipe']['name'] = message.text
            bot.send_message(message.chat.id, 'Отлично! Какие ингредиенты?')
        elif 'ingredients' not in user_session['add_recipe']:
            user_session['add_recipe']['ingredients'] = message.text
            bot.send_message(message.chat.id, 'Отлично! Добавь описание')
        elif 'description' not in user_session['add_recipe']:
            user_session['add_recipe']['description'] = message.text
            recipe_data = user_session['add_recipe']
            text = '\n\n'.join(
                (
                    recipe_data['name'],
                    recipe_data['ingredients'],
                    recipe_data['description']
                )
            )
            markup = t.types.InlineKeyboardMarkup()
            save_btn = t.types.InlineKeyboardButton(
                'Сохранить', callback_data='save_recipe'
            )
            markup.add(save_btn)
            bot.send_message(message.chat.id, text, reply_markup=markup)



@bot.callback_query_handler(func=lambda callback: callback.data == 'save_recipe')
def handle_save_recipe_query(callback):
    recipe_data = telegram_session[callback.from_user.id]['add_recipe']
#   new_recipe = Recipe(message_id=callback.data.split(',')[1])
#   session.add(new_recipe)
#   session.commit()

    chat_id = callback.message.chat.id
    # bot.edit_message_text('Заебись рецепт! Сохранить?', chat_id, callback.message.id)
    bot.send_message(chat_id, "Сохранено!")


# @bot.message_handler(commands=['random'])
# @message_auth
# def get_random_recipe(message):
#     bot.forward_message(message.chat.id, message.chat.id, random.choice(recipes))



