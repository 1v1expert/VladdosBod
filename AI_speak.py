from telebot import *
from config import *
import grab

bot = TeleBot(TELEGRAM_TOKEN)

g = grab.Grab()
g.go('http://aiproject.ru/')

@bot.message_handler(commands=['start'])
def init(message):
    try:
        bot.send_message(message.chat.id, work_with_alice("Привет"))
    except:
        bot.send_message(message.chat.id, "Прощайте, не хочу с Вами разговаривать")

@bot.message_handler(content_types=["text"])
def get_message_answer(message):
    try:
        bot.send_message(message.chat.id, work_with_alice(message.text))
    except:
        bot.send_message(message.chat.id, "Я отдыхаю, отдохните и Вы")

def work_with_alice(answer):
    g.set_input_by_id('askMe', answer)
    g.submit()
    return g.xpath_text('//*[@id="top"]/div/div[2]/p[3]')[6:]

if __name__=='__main__':
    bot.polling(none_stop=True)
    