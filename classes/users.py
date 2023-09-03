from classes.storage import Loader, NamesStorage


class Users:
    file_way = "files/storage.json"

    @classmethod
    def authorize(cls, user_id, user_group):
        cls.delete_user_data(user_id)
        cls.__put_user_data_to_file(user_id, user_group)

    @classmethod
    def delete_user_data(cls, user_id):
        file = Loader.load_data(cls.file_way)
        if str(user_id) in file:
            del file[str(user_id)]
            Loader.save_data(file, cls.file_way)

    @classmethod
    def __put_user_data_to_file(cls, user_id, user_group):
        file = Loader.load_data(cls.file_way)
        file[user_id] = {NamesStorage.user_group: user_group, NamesStorage.remind: True}
        Loader.save_data(file, cls.file_way)

    @classmethod
    def get_info_by_user_id(cls, user_id):
        return Loader.load_data(cls.file_way)[str(user_id)]

    @classmethod
    def get_group_by_user_id(cls, user_id):
        return cls.get_info_by_user_id(user_id)[NamesStorage.user_group]

    @classmethod
    def get_remind_by_user_id(cls, user_id):
        return cls.get_info_by_user_id(user_id)[NamesStorage.remind]

    @classmethod
    def switch_on_remind_by_user_id(cls, user_id):
        file = Loader.load_data(cls.file_way)
        file[str(user_id)][NamesStorage.remind] = True
        Loader.save_data(file, cls.file_way)

    @classmethod
    def switch_off_remind_by_user_id(cls, user_id):
        file = Loader.load_data(cls.file_way)
        file[str(user_id)][NamesStorage.remind] = False
        Loader.save_data(file, cls.file_way)
