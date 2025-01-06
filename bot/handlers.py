from bot.bot import bot
import telebot as t
from bot.auth import message_auth

from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from bot.models import engine, Recipe

DBSession = sessionmaker(bind=engine)
db_session = DBSession()


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


@bot.message_handler(commands=['random_recipe'])
@message_auth
def get_random_recipe(message):
    recipe = db_session.query(Recipe).order_by(func.random()).first()
    text = '\n\n'.join((recipe.name, recipe.ingredients, recipe.description))
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['find_ingredient'])
@message_auth
def find_ingredient(message):
    telegram_session[message.from_user.id] = {'find_ingredient': {}}
    bot.send_message(message.chat.id, 'Какой ингредиент ищешь?')



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

    elif 'find_ingredient' in user_session:
        search_string = message.text

        recipes = db_session.query(Recipe).filter(
            Recipe.ingredients.contains(search_string)
        ).all()

        markup = t.types.InlineKeyboardMarkup()
        for recipe in recipes:
            recipe_btn = t.types.InlineKeyboardButton(
                recipe.name, callback_data=f'get_recipe,{recipe.id}'
            )
            markup.add(recipe_btn)

        bot.send_message(message.chat.id, 'Результаты поиска:', reply_markup=markup)



@bot.callback_query_handler(func=lambda callback: callback.data == 'save_recipe')
def handle_save_recipe_query(callback):
    recipe_data = telegram_session[callback.from_user.id]['add_recipe']
    new_recipe = Recipe(**recipe_data)
    db_session.add(new_recipe)
    db_session.commit()

    bot.send_message(callback.message.chat.id, 'Сохранено!')

@bot.callback_query_handler(func=lambda callback: callback.data.split(',')[0] == 'get_recipe')
def handle_get_recipe_query(callback):
    recipe_id = callback.data.split(',')[1]
    recipe = db_session.query(Recipe).get(recipe_id)
    text = '\n\n'.join((recipe.name, recipe.ingredients, recipe.description))
    bot.send_message(callback.message.chat.id, text)
