from telebot import types
from classes.debug import Debug
from classes.users import Users
from classes.tools import BackTool
from classes.storage import Loader, NamesStorage
from classes.main_init import bot, Data, Parser, server_sec_shift


class BotCommands:
    def __init__(self):
        self.commands = ["start", "info", "group", "today", "tomorrow", "week", "nextweek", "prep", "remind", "debug"]

        @bot.message_handler(commands=['start'])
        def welcome(message):
            Users.authorize(user_id=message.chat.id, user_group=list(Parser.parse(0).keys())[0])
            bot.send_message(message.chat.id,
                             "Вітаю, <b>{0.first_name}!</b>\n"
                             "Мене було створено, щоб допомогти Вам відстежувати свій розклад. "
                             "Переглянути доступні команди можна за допомогою клавіші "
                             '<b>"Меню"</b> у нижньому лівому кутку, або натиснувши сюди <b> /info </b>.\n'
                             ''.format(message.from_user, bot.get_me()),
                             parse_mode='html')
            set_group(message)

        @bot.message_handler(commands=['info'])
        def info(message):
            bot.send_message(message.chat.id,
                             "<b>Список команд:</b>\n"
                             "/start - запустити бота\n"
                             "/info - список команд\n"
                             "/group - змінити групу\n"
                             "/prep - інформація про викладачів\n"
                             "/remind - управління сповіщеннями\n"
                             "/today - пари на сьогоді\n"
                             "/tomorrow - пари на завтра\n"
                             "/week - пари на неділю\n"
                             "/nextweek - пари на наступну неділю\n"
                             .format(message.from_user, bot.get_me()),
                             parse_mode='html')

        @bot.message_handler(commands=['group'])
        def set_group(message):
            groups = Parser.parse(0).keys()
            markup = types.InlineKeyboardMarkup(row_width=3)
            for group_name in groups:
                button = types.InlineKeyboardButton(group_name, callback_data=group_name)
                markup.add(button)

            bot.send_message(message.chat.id,
                             "Будь ласка, оберіть свою групу.".format(message.from_user, bot.get_me()),
                             reply_markup=markup)

        @bot.message_handler(commands=['today'])
        def today(message):
            today_sch = BackTool.beautified_today_info(Data.today_group_schedule(message.chat.id, server_sec_shift))
            if len(today_sch) == 0:
                bot.send_message(message.chat.id, "Сьогодні пари відсутні!")
            else:
                for lesson in today_sch:
                    bot.send_message(message.chat.id, lesson, parse_mode='html', disable_web_page_preview=True)

        @bot.message_handler(commands=['tomorrow'])
        def tomorrow(message):
            today_sch = BackTool.beautified_today_info(
                Data.today_group_schedule(message.chat.id, shift=86400 + server_sec_shift))
            if len(today_sch) == 0:
                bot.send_message(message.chat.id, "Завтра пари відсутні!")
            else:
                for lesson in today_sch:
                    bot.send_message(message.chat.id, lesson, parse_mode='html', disable_web_page_preview=True)

        @bot.message_handler(commands=['week'])
        def week(message):
            week_sch = BackTool.beautified_week_info(
                Data.week_group_schedule(message.chat.id, shift=server_sec_shift / 3600))
            for lesson in week_sch:
                bot.send_message(message.chat.id, lesson, parse_mode='html', disable_web_page_preview=True)

        @bot.message_handler(commands=['nextweek'])
        def nextweek(message):
            week_sch = BackTool.beautified_week_info(
                Data.week_group_schedule(message.chat.id, shift=168 + server_sec_shift / 3600))
            for lesson in week_sch:
                bot.send_message(message.chat.id, lesson, parse_mode='html', disable_web_page_preview=True)

        @bot.message_handler(commands=['prep'])
        def prep(message):
            bot.send_message(message.chat.id, BackTool.beautified_prep_info(Parser.prep_parse()), parse_mode='html',
                             disable_web_page_preview=True)

        @bot.message_handler(commands=['remind'])
        def reminder(message):
            markup = types.InlineKeyboardMarkup(row_width=2)
            button_yes = types.InlineKeyboardButton("Так", callback_data="Так")
            button_no = types.InlineKeyboardButton("Ні", callback_data="Ні")
            markup.add(button_yes, button_no)

            persons = Loader.load_data(NamesStorage.load_way)
            if persons[str(message.chat.id)]["remind"]:
                bot.send_message(message.chat.id, "Нагадувач працює. Вимкнути?", reply_markup=markup)
            else:
                bot.send_message(message.chat.id, "Нагадувач вимкнено. Увімкнути?", reply_markup=markup)

        @bot.callback_query_handler(func=lambda call: True)
        def callback_inline(call):
            if call.message.text == "Будь ласка, оберіть свою групу.":
                self.group_selection(call)

            elif call.message.text == "Нагадувач працює. Вимкнути?":
                self.reminder_turn_off(call)

            elif call.message.text == "Нагадувач вимкнено. Увімкнути?":
                self.reminder_turn_on(call)

        @bot.message_handler(content_types=['document'])
        def set_new_file(message):
            Debug(message).change_file()

        @bot.message_handler(content_types=['text'])
        def reaction(message):
            Debug(message).debug_by_commands()

    @staticmethod
    def group_selection(call):
        group = call.data
        # Remove inline buttons
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Ви обрали групу.", reply_markup=None)
        # Add user to base
        Users.authorize(user_id=call.message.chat.id, user_group=group)

    @staticmethod
    def reminder_turn_off(call):
        sbj_name = call.data
        if sbj_name == "Так":
            Users.switch_off_remind_by_user_id(call.message.chat.id)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Нагадувач вимкнено.", reply_markup=None)
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Нагадувач працює.", reply_markup=None)

    @staticmethod
    def reminder_turn_on(call):
        sbj_name = call.data
        if sbj_name == "Так":
            Users.switch_on_remind_by_user_id(call.message.chat.id)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Нагадувач увімкнено.", reply_markup=None)
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Нагадувач вимкнено.", reply_markup=None)