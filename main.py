import os
import telebot
from dotenv import load_dotenv
from pyowm import OWM
import schedule
import time

load_dotenv()

bot = telebot.TeleBot(os.getenv('TELEGRAM_TOKEN'))
owm = OWM(os.getenv('OWM_API_KEY'))

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, я бот-погода! Напиши мне название города и я скажу тебе, какая погода сейчас там.')

@bot.message_handler(content_types=['text'])
def send_weather(message):
    mgr = owm.weather_manager()
    try:
        observation = mgr.weather_at_place(message.text)
        w = observation.weather
        temperature = w.temperature('celsius')['temp']
        answer = f"В городе {message.text} сейчас {w.detailed_status}, температура воздуха {temperature:.1f}°C"
    except:
        answer = "Я не смог узнать погоду в этом городе, попробуйте еще раз"
    bot.send_message(message.chat.id, answer)

def send_daily_weather():
    city = "Moscow" # здесь указать город, для которого отправлять погоду
    mgr = owm.weather_manager()
    try:
        observation = mgr.weather_at_place(city)
        w = observation.weather
        temperature = w.temperature('celsius')['temp']
        answer = f"В городе {city} сейчас {w.detailed_status}, температура воздуха {temperature:.1f}°C"
        bot.send_message(os.getenv('TELEGRAM_CHAT_ID'), answer)
    except:
        answer = "Я не смог узнать погоду в этом городе, попробуйте еще раз"
        bot.send_message(os.getenv('TELEGRAM_CHAT_ID'), answer)

# Отправляем погоду в 9 утра каждый день
schedule.every().day.at("09:00").do(send_daily_weather)

while True:
    schedule.run_pending()
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(5)
