from config import *
from telebot import *
import emoji

bot = TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(content_types=["contact"])
def autorization(message):
    bot.send_message(message.chat.id, "Спасибо, что авторизовались")

def get_specifiec_keyboard(chat_id, caption):
    keyboard_phone = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
    keyboard_phone.add(button_phone)
    bot.send_message(chat_id, caption, reply_markup=keyboard_phone)
    
def start_menu(chat_id, caption):
    menu = types.InlineKeyboardMarkup()
    get_info = types.InlineKeyboardButton(text='Инфо по отправлению', callback_data='get_info_order')
    get_contacts = types.InlineKeyboardButton(text='Контакты', callback_data='get_contact')
    menu.add(get_info, get_contacts)
    bot.send_message(chat_id, "Получите информацию по отправлению или контакты тех поддержки",
                     reply_markup=menu)

@bot.message_handler(commands=['start'])
#@bot.message_handler(func=lambda msg: msg.text.encode("utf-8") == SOME_FANCY_EMOJI)
def send_something(message):
    get_specifiec_keyboard(message.chat.id, "Авторизируйтесь или получите информацию по отправлению")
    start_menu(message.chat.id, "SS")
    
    print(message)
    
@bot.message_handler(content_types=["text"])
def await_number_parcel(message):
    import requests_IS
    response = requests_IS.get_info(TOKEN_TEST, '{0}/parcels?offset=0&limit=25&order_id={1}'.format(DEV_URL, message.text))
    print(response.json()['results'])
    

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        if call.data == 'get_contact':
            #bot.send_message(call.message.chat.id, )
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Телефон обратной связи: 8 800 511 92 63"
            )
        elif call.data == 'get_info_order':
            bot.send_message(call.message.chat.id, "Введите номер отправления:")
            #start_menu(call.message.chat.id, 'sd')

@bot.message_handler(commands=['hide'])
def send_someth(message):
    markup = types.ForceReply(selective=False)
    bot.send_message(message.chat.id, "Send me another word:", reply_markup=markup)
    
if __name__ == '__main__':
    bot.polling(none_stop=True)