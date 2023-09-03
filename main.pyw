from time import sleep
from classes.notification_sender import NotificationsSender
from classes.bot_commands import BotCommands
from classes.main_init import bot


class Main(BotCommands):
    def __init__(self):
        super().__init__()
        self.warnings_schedule = NotificationsSender()
        self.warnings_schedule_thread = self.warnings_schedule.run_schedule()

    @staticmethod
    def run():
        while True:
            try:
                bot.polling()
            except Exception as e:
                print("~~~~~~Pooling error~~~~~~")
                print(e)


main = Main()

while True:
    try:
        main.run()
    except Exception as e:
        print(e)
        sleep(3)
