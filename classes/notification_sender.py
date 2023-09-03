from threading import Thread
import schedule
from time import sleep
from classes.tools import BackTool
from classes.storage import Loader, NamesStorage
from classes.main_init import *
from classes.users import Users


class NotificationsSender:
    def __init__(self):
        self.lessons_start_time = ["08:57", "10:27", "12:07", "13:37", "15:07", "16:37", "18:07"]

    @staticmethod
    def warn_users_about_lesson():
        print("---Start notification sending")
        time_now = str(BackTool.get_curr_time_str(add_hour=server_sec_shift / 3600, add_min=3))

        users = Loader.load_data(NamesStorage.load_way)
        for user_id in users:
            today_sch = BackTool.beautified_today_info(Data.today_group_schedule(user_id, shift=server_sec_shift))
            if users[user_id]["remind"]:
                for lesson in today_sch:
                    if lesson[3:8] == time_now:
                        try:
                            bot.send_message(user_id, "<b>Нагадую, через 3 хвилини розпочинається пара:</b>",
                                             parse_mode='html')
                            bot.send_message(user_id, lesson, parse_mode='html')
                            print("Message sent to ", user_id)
                        except Exception as e:
                            if e.error_code == 403:
                                Users.delete_user_data(user_id)
                            print(e)
                            print("Message sent error: ", user_id)
                        break

    def run_schedule(self):
        for lesson_start_time in self.lessons_start_time:
            schedule.every().day.at(lesson_start_time).do(self.warn_users_about_lesson)

        def message_reminder():
            while True:
                schedule.run_pending()
                sleep(2)

        thread = Thread(target=message_reminder)
        thread.start()
        return thread
