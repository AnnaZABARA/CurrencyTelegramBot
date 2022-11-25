import telebot  #импортируем библиотеку, для работы с Телеграм-ботами
from configur import keys,TOKEN #импортируем из файла записанный словарь со значениями и токен, созданного Телеграм-бота
from extensions import CurrencyException, CurrencyConverter #импортируем исключения на ошибки пользователя из файла

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start']) #задаем команду при старте бота
def start(message: telebot.types.Message):
    text = 'Что может делать данный бот? \n Привет! Я бот, который умеет конвертировать валюту и я могу\n- Показать список доступных валют через команду /values \
    \n- Вывести конвертацию валюты через команду <имя валюты> <в какую валюту перевести> <количество переводимой валюты>\n \
- Напомнить, что я могу через команду /help'
    bot.reply_to(message, text)

@bot.message_handler(commands=['help']) # задаем команду при вводe /help
def help(message: telebot.types.Message):
    text = 'Чтобы начать конвертацию, введите команду боту в следующем формате: \n<имя валюты> <в какую валюту перевести> <количество переводимой валюты>\nЧтобы увидеть список всех доступных валют, введите команду\n/values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values']) # задаем команду при вводe /values вывести валюты из словаря
def values(message: telebot.types.Message):
    text = 'Доступные валюты'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text']) # задаем основную команду при вводе валидных данных
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise CurrencyException('Введите три параметра')

        quote, base, amount = values
        total_base = CurrencyConverter.get_price(quote, base, amount)
    except CurrencyException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e} ')
    else:
        text = f'Перевод {amount} {quote} в {base} - равен {total_base}'
        bot.send_message(message.chat.id, text)



bot.polling()
