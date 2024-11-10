from bot import bot
from settings import DENIS_ID, DASHA_ID


def message_auth(message_handler):
    def wrapper(message):
        if str(message.from_user.id) not in (DASHA_ID, DENIS_ID):
            bot.reply_to(message, 'Это не твой бот!')
        else:          
            message_handler(message)
    
    return wrapper