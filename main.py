import telebot
import pyowm
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# Получаем токен бота и API ключ погоды из переменных окружения
bot_token = os.getenv('BOT_TOKEN')
owm_api_key = os.getenv('OWM_API_KEY')


# Устанавливаем токен бота и API погоды
bot = telebot.TeleBot(bot_token)
owm = pyowm.OWM(owm_api_key)

# Задаем город и язык для запроса погоды
city = 'Moscow, RU'
language = 'ru'

# Получаем прогноз погоды на сегодня и завтра
def get_weather_forecast():
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = today + timedelta(days=1)
    fc = owm.three_hours_forecast(city)
    forecast_today = fc.get_weather_at(today).get_detailed_status()
    forecast_tomorrow = fc.get_weather_at(tomorrow).get_detailed_status()
    return f'Погода на сегодня: {forecast_today}\nПогода на завтра: {forecast_tomorrow}'

# Отправляем сообщение в заданное время
@bot.message_handler(commands=['start'])
def send_weather_forecast(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, get_weather_forecast())

bot.polling(none_stop=True)
