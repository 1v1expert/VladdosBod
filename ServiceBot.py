from telebot import TeleBot
from telebot import types
from config import TELEGRAM_TOKEN, TEST_GROUP_ID, GROUP_ID
import random

bot = TeleBot(TELEGRAM_TOKEN)

#
# @bot.message_handler(commands=['start'])
# def init(message):
# 	bot.send_message(message.chat.id, "Привет, {} {}".format(message.chat.first_name, message.chat.last_name))
#
#
# @bot.message_handler(content_types=["text"])
# def get_message_answer(message):
# 	bot.send_message(message.chat.id, "Message:/n {}".format(message))
#
#
# if __name__ == '__main__':
# 	bot.polling(none_stop=True)

user_dict = {}
ch_msg = ['Я пока не готов с тобой пообщаться, погоди пока меня закончат',
          'Я очень рад, что ты попался довольно общительный, но данный функционал ещё в разработке',
          'Мм, тебе скучно, давай пообщаемся, но в другой раз']
stickers = ['CAADAgADfx8AAulVBRi8dixJA2XkPhYE', 'CAADAgADex8AAulVBRjkuOTEW319pBYE', 'CAADAgADhR8AAulVBRiL1RvzSAWMyBYE']


class Request:
    def __init__(self, number):
        self.number = number
        self.reason = None
        self.number_point = None
        self.status = None
        # self.sex = None


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    msg = bot.reply_to(message, "Привет, {} {}\n "
                                "Если хочешь создать заявку на изменение статуса, то напиши мне /new.\n"
                                "Если же хочешь просто поболтать, то напиши мне /Talk_to_me".format(message.chat.first_name, message.chat.last_name))
    # bot.register_next_step_handler(msg, process_name_step)
    
    
# @bot.message_handler(content_types=['sticker'])
# def send_text(message):
#     bot.reply_to(message, 'msg: {}'.format(message.sticker.file_id))
#     bot.send_sticker(data='CAADAgADjB8AAulVBRhLQxc-nazzzRYE', chat_id=message.chat.id)

@bot.message_handler(content_types=['sticker'])
def send_sticker(message):
    bot.send_sticker(data=stickers[random.randint(0, len(stickers) - 1)], chat_id=message.chat.id)


@bot.message_handler(commands=['Talk_to_me'])
def process_create_request(message):
    msg = bot.reply_to(message, ch_msg[random.randint(1, len(ch_msg))-1])
    bot.send_sticker(data=stickers[random.randint(0, len(stickers)-1)], chat_id=message.chat.id)
    bot.send_sticker(data=stickers[random.randint(0, len(stickers) - 1)], chat_id=TEST_GROUP_ID)


@bot.message_handler(commands=['new'])
def process_create_request(message):
    msg = bot.reply_to(message, "Какой номер отправления?")
    bot.register_next_step_handler(msg, process_number_step)


def process_number_step(message):
    try:
        chat_id = message.chat.id
        number = message.text
        request_order = Request(number)
        user_dict[chat_id] = request_order
        msg = bot.reply_to(message, 'Какой номер почтомата?')
        bot.register_next_step_handler(msg, process_number_point_step)
    except Exception as e:
        bot.reply_to(message, 'oooops, что-то пошло не так')


def process_number_point_step(message):
    try:
        chat_id = message.chat.id
        number_point = message.text
        if not number_point.isdigit():
            msg = bot.reply_to(message, 'Номер почтомата должен состоять исключительно из цифр')
            bot.register_next_step_handler(msg, process_number_point_step)
            return
        user = user_dict[chat_id]
        user.number_point = number_point
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Доставлено', 'Получено')
        msg = bot.reply_to(message, 'На какой статус изменить?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_status_step)
    except Exception as e:
        bot.reply_to(message, 'oooops, что-то пошло не так')


def process_status_step(message):
    try:
        chat_id = message.chat.id
        status = message.text
        user = user_dict[chat_id]
        if (status == u'Доставлено') or (status == u'Получено'):
            user.status = status
        else:
            msg = bot.reply_to(message, 'Неверный ввод, пожалуйста выбери один из вариантов')
            bot.register_next_step_handler(msg, process_status_step)
            return
            # bot.register_next_step_handler(message, process_number_point_step)
            # raise Exception()
        mm = 'Отлично! Заявка №{} создана. \n Отправление: {}\n Почтомат: {}\n Статус: {}'.format(
            random.randint(9999, 99999),
            user.number,
            user.number_point,
            user.status,
            user.status)
        bot.send_message(chat_id,
                         mm)
        bot.send_message(TEST_GROUP_ID, mm)
        bot.send_message(GROUP_ID, mm)
    except Exception as e:
        bot.reply_to(message, 'oooops, что-то пошло не так')


# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.polling()
# https://github.com/eternnoir/pyTelegramBotAPI/blob/master/examples/step_example.py