from classes.parser import Parser as Ps
from classes.users import Users
from classes.tools import BackTool


class Data:
    def __init__(self):
        self.Parser = Ps()

    def week_group_schedule(self, user_id, shift=0):
        ipz_schedule = self.Parser.parse(shift)
        return ipz_schedule[Users.get_group_by_user_id(user_id)]

    def today_group_schedule(self, user_id, shift=0):
        ipz_schedule = self.Parser.parse(shift)[Users.get_group_by_user_id(user_id)]
        a = BackTool.rename_day(BackTool.get_time_dict(shift=shift)['day'])
        return ipz_schedule[a]
