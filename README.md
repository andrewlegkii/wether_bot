# PYTHON WEATHER BOT
Проект выполнен на Python с использованием дополнительных библиотек.
Проект представляет собой телеграм-бот для получения информации о погоде в том или ином месте(городе).
Добавлена возможность регулярно получать уведобление о погоде в Москве в 09:00 по МСК.

# Как установить

1. Клонировать репозиторий: git clone https://github.com/andrewlegkii/wether_bot.git
2. Установить виртуальное окружение: python -m venv venv
3. Активировать виртуальное окружение: source venv/Scripts/activate
4. Выполнить установку необходимы библиотек для работы проекта: pip install -r requirements.txt
5. Создайте файл .env и добавте в данный файл следующие данные: TELEGRAM_TOKEN, OWM_API_KEY, TELEGRAM_CHAT_ID
6. Запуск бота: python main.py

# Как использовать

После установки и настройки бота необходимо запустить бот командой /start и ввести город, в котором вы хотели бы узнать погоду.

# Авторы

Андрей Легкий - https://github.com/andrewlegkii