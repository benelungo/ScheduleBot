import json


class Loader:
    @classmethod
    def save_data(cls, data_to_save, file_way):
        save_file = open(file_way, 'w+')
        save_file.seek(0)
        save_file.write(json.dumps(data_to_save))

    @classmethod
    def load_data(cls, file_way):
        load_file = open(file_way, 'r+')
        loaded_data = json.loads(load_file.read())
        return loaded_data

    @classmethod
    def clear_data(cls, file_way):
        save_file = open(file_way, 'w+')
        save_file.seek(0)


class NamesStorage:
    # User data
    user_id = 'user_id'
    user_group = 'user_group'
    remind = 'remind'
    # Links
    load_way = 'files/storage.json'
    stat_way = 'files/stat.json'
