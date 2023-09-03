import os
import time
from classes.main_init import bot, super_key, server_sec_shift, schedule_file_path, prep_info_path, Parser, Data


class Debug:
    def __init__(self, message):
        self.message = message
        self.command_links = {"exit": lambda: self._exit(),
                              "debug": lambda: self._debug_info(),
                              "help": lambda: self._help(),
                              "files": lambda: self._get_data_files(),
                              "reset": lambda: self._reset_data()}

    def change_file(self):
        file_name = self.message.document.file_name
        file_id = self.message.document.file_id
        file_caption = self.message.caption
        if (file_name == "ipz_schedule.xlsx" or file_name == "prep_info.xlsx") and file_caption == str(super_key):
            file_info = bot.get_file(file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open("files/" + file_name, 'wb') as file:
                file.write(downloaded_file)
            bot.send_message(self.message.chat.id, file_name + " was replaced!")
            self._reset_data()

    def debug_by_commands(self):
        key = str(self.message.text[:len(str(super_key))])
        if key != str(super_key):
            return False
        else:
            message_text = self.message.text
            command = message_text[len(str(super_key)):].strip()
            if command not in self.command_links:
                self._wrong_command()
            else:
                self.command_links[command]()

    def _exit(self):
        print("Closed by user: " + "\n    Username: " + self.message.chat.username + "\n    ID: " + str(
            self.message.chat.id))
        os._exit(1)

    def _debug_info(self):
        server_time = time.ctime(time.time()).split()
        real_time = time.ctime(time.time() + server_sec_shift).split()
        bot.send_message(self.message.chat.id, f"<b>User id:</b> {str(self.message.chat.id)}", parse_mode="html")
        bot.send_message(self.message.chat.id, "<b>Server time:</b> " + ' '.join(server_time), parse_mode="html")
        bot.send_message(self.message.chat.id, "<b>Real time:</b> " + ' '.join(real_time), parse_mode="html")

    def _help(self):
        answer = "Commands:"
        for command in self.command_links.keys():
            answer += "\n" + str(command)

        bot.send_message(self.message.chat.id, answer)

    def _wrong_command(self):
        print("Wrong command: " + self.message.text)
        bot.send_message(self.message.chat.id, "Wrong command!")

    def _get_data_files(self):
        schedule_file = open(schedule_file_path, 'rb')
        prep_file = open(prep_info_path, 'rb')
        bot.send_document(self.message.chat.id, schedule_file)
        bot.send_document(self.message.chat.id, prep_file)

    def _reset_data(self):
        Parser.__init__()
        Data.__init__()
        bot.send_message(self.message.chat.id, "Data was reset!")
