import telebot
import random
from classes import config
from classes.community import Data as Dt
from classes.parser import Parser as Ps

bot = telebot.TeleBot(config.TOKEN)
Data = Dt()
Parser = Ps()
server_sec_shift = 0
super_key = 0  # random.randint(1000, 9999)
schedule_file_path = r'files/ipz_schedule.xlsx'
prep_info_path = r'files/prep_info.xlsx'
print(super_key)
