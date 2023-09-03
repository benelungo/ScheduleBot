import time
from math import ceil
import calendar


class BackTool:
    @classmethod
    def week_of_study(cls, hours_shift=0):
        year = time.gmtime().tm_year
        months_days = [calendar.monthrange(year, i+1)[1] for i in range(12)]
        months = {"Sep": 1, "Oct": 2, "Nov": 3, "Dec": 4, "Jan": 5, "Feb": 6, "Mar": 7, "Apr": 8, "May": 9,
                  "Jun": 10, "Jul": 11, "Aug": 12}

        now = time.ctime(time.time()).split()
        study_time_hours = int(now[2]) * 24 + int(now[3].split(":")[0]) + hours_shift
        for i in range(months[now[1]] - 1):
            study_time_hours += months_days[i] * 24
        return ceil(study_time_hours / 24 / 7)

    @classmethod
    def get_time_dict(cls, shift=0):
        now = time.ctime(time.time() + shift).split()
        now_time = [int(now[3].split(":")[i]) for i in range(3)]
        return {"day": now[0], "hours": int(now_time[0]), "minutes": now_time[1], "seconds": now_time[2]}

    @classmethod
    def get_curr_time_str(cls, add_hour=0, add_min=0):
        curr_time = str(BackTool.get_time_dict()["hours"] + int(add_hour)) + ":" + str(BackTool.get_time_dict()["minutes"] + int(add_min))
        if len(curr_time) == 4:
            curr_time = "0" + curr_time
        return curr_time

    @classmethod
    def rename_day(cls, day):
        return {"Mon": "Понеділок", "Tue": "Вівторок", "Wed": "Середа", "Thu": "Четвер", "Fri": "П'ятниця", "Sat": "Субота", "Sun": "Неділя"}[day]

    @classmethod
    def beautified_today_info(cls, lesson):
        ret = []
        for key in lesson.keys():
            if str(lesson[key]['Пара']) != 'nan':
                ret.append(
                    '<b>%(1)s</b>\n%(2)s\n%(3)s' % {'1': key, '2': lesson[key]['Пара'], '3': lesson[key]['Аудиторія']})
        return ret

    @classmethod
    def beautified_week_info(cls, week_schedule):
        ret = []
        k = 0
        for day in week_schedule.keys():
            ret.append('<i><b>%s:</b></i>' % day)
            for key in week_schedule[day].keys():
                if str(week_schedule[day][key]['Пара']) != 'nan':
                    ret[k] += ('\n<b>%(1)s</b>\n%(3)s\n%(2)s\n' % {'1': key, '2': week_schedule[day][key]['Аудиторія'], '3': week_schedule[day][key]['Пара']})
            if ret[k] == '<i><b>' + day + ':</b></i>':
                ret[k] += " Пари відсутні!"
            k += 1
        return ret

    @classmethod
    def beautified_prep_info(cls, prep_info):
        line = ''
        for prep in prep_info:
            line += "<b>%(1)s</b>\n   - %(2)s\n" % {'1': prep[0], '2': prep[1]}
        return line
