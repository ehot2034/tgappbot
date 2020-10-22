import telebot
import pyowm
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
from pyowm.utils.config import get_default_config

config_dict = get_default_config()
config_dict['language'] = 'ru' 

owm = pyowm.OWM('6d00d1d4e704068d70191bad2673e0cc')
mgr = owm.weather_manager()
bot = telebot.TeleBot("1333118982:AAHZDvk-hwSrR8a0iYXfD49FfBcYmEjfkyo") # You can set parse_mode by default. HTML or MARKDOWN

keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True )
keyboard1.row("/pogoda")

goroda = telebot.types.ReplyKeyboardMarkup(True, True )
goroda.row("Москва", "Новомосковск", "Тула")

@bot.message_handler(commands=["start"])
def start_message(message):
	bot.send_message(message.chat.id, 'Привет\nЭтот бот показывает осадки, температуру и скорость ветра в любом существующем городе!\nДля начала введи /pogoda', reply_markup=keyboard1)

@bot.message_handler(commands=["pogoda"])
def send_pogoda(message):
	bot.send_message(message.chat.id, "Выберите название города: ",  reply_markup=goroda)
	bot.register_next_step_handler(message, pogoda)

@bot.message_handler()
def pogoda(message):
	place = message.text
	try:
		observation = mgr.weather_at_place(place)
		w = observation.weather
		wild = w.wind('meters_sec')["speed"]
		wild = round(wild)
		temp = w.temperature('celsius')['temp']
		temp = round(temp)
		stat = observation.weather.detailed_status
		str(stat)

		if wild == 1:
			wmd = str("метр")
		elif temp == 2:
			wmd = str("метра")
		elif wild == 3:
			wmd = str("метра")
		elif wild == 4:
			wmd = str("метра")
		else:
			wmd = str("метров")

		if temp == 1:
			gradus = str("градус")
		elif temp == 2:
			gradus = str("градуса")
		elif temp == 3:
			gradus = str("градуса")
		elif temp == 4:
			gradus = str("градуса")
		else:
			gradus = str("градусов")

		answer = "В городе " + place + " "+ str(stat) + "\n"
		answer += str(temp) + " " + gradus + " по цельсию" +"\n"
		answer += "Ветер со скоростью " + str(wild) + " " + wmd + " в секунду"
		bot.send_message(message.chat.id, answer)
	except:
		bot.send_message(message.chat.id,'Ошибка! Город не найден.')
		return



bot.polling(none_stop=True)