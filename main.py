import os
import telebot
from dotenv import load_dotenv
from pyowm import OWM
import schedule
import time

load_dotenv()

bot = telebot.TeleBot(os.getenv('TELEGRAM_TOKEN'))
owm = OWM(os.getenv('OWM_API_KEY'))

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
    keyboard.add("Москва")
    bot.send_message(message.chat.id, 'Привет, я бот-погода! Напиши мне название города и я скажу тебе, какая погода сейчас там.', reply_markup=keyboard)

# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def send_weather(message):
    mgr = owm.weather_manager()
    try:
        observation = mgr.weather_at_place(message.text)
        w = observation.weather
        temperature = w.temperature('celsius')['temp']
        answer = f"В городе {message.text} сейчас {w.detailed_status}, температура воздуха {temperature:.1f}°C"
        if temperature < 0:
            answer += ", лучше надеть зимнюю куртку, шарф и перчатки."
        elif temperature < 10:
            answer += ", лучше надеть теплую куртку, толстовку или футболку с кофтой."
        elif temperature < 20:
            answer += ", лучше надеть легкую куртку с футболкой или свитер."
        else:
            answer += ", лучше надеть легкую одежду."
    except:
        answer = f"Я не смог узнать погоду в городе {message.text}, попробуйте еще раз"
    bot.send_message(message.chat.id, answer)

# Функция отправки ежедневной погоды
def send_daily_weather():
    city = os.getenv('CITY_NAME')
    mgr = owm.weather_manager()
    try:
        observation = mgr.weather_at_place(city)
        w = observation.weather
        temperature = w.temperature('celsius')['temp']
        answer = f"В городе {city} сейчас {w.detailed_status}, температура воздуха {temperature:.1f}°C"
        bot.send_message(os.getenv('TELEGRAM_CHAT_ID'), answer)
    except:
        answer = f"Я не смог узнать погоду в городе {city}, попробуйте еще раз"
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
