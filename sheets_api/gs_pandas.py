import apiclient
import httplib2
import pandas as pd

from sql_data.sql import session, WorkTime, Employee
from datetime import datetime as dt
from oauth2client.service_account import ServiceAccountCredentials
from config_data.secret import google_token, spreadsheet_ID
from config_data.fltrs import industrial_calendar


class GS:
    """Получение таблиц из google sheets"""

    __google_sheets_token = google_token
    __spreadsheet_ID = spreadsheet_ID
    __credentials = ServiceAccountCredentials.from_json_keyfile_dict(__google_sheets_token,
                                                                     ["https://www.googleapis.com/auth/spreadsheets",
                                                                      "https://www.googleapis.com/auth/drive"])
    __httpauth = __credentials.authorize(httplib2.Http())
    __service = apiclient.discovery.build('sheets', 'v4', http=__httpauth)
    __spreadsheet_info = __service.spreadsheets().get(spreadsheetId=__spreadsheet_ID).execute()
    month_list = ['', 'янв', 'фев', 'мар', 'апр', 'май', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']

    def __init__(self, month: int = dt.now().month, year: int = dt.now().year):
        self.__month = month
        self.__year = str(year)[-2::]

    @classmethod
    def get_list_name(cls) -> list:
        s_i = cls.__spreadsheet_info
        return [s_i['sheets'][i]['properties']['title'] for i in range(len(s_i['sheets']))]

    def get_current_list(self) -> str:
        for g_list in self.get_list_name():
            if self.month_list[self.__month] in g_list.lower() and self.__year in g_list:
                return g_list

    def get_amount_rows(self, list_name: str) -> int:
        for rs_i in range(len(self.__spreadsheet_info['sheets'])):
            if self.__spreadsheet_info['sheets'][rs_i]['properties']['title'] == list_name:
                return self.__spreadsheet_info['sheets'][rs_i]['properties']['gridProperties']['rowCount']

    def get_spreadsheet_values(self) -> list:
        list_name = self.get_current_list()
        amount_rows = self.get_amount_rows(list_name)
        return self.__service.spreadsheets().values().get(spreadsheetId=self.__spreadsheet_ID,
                                                          range=f'{list_name}!A1:FC{amount_rows}',
                                                          majorDimension='ROWS').execute()['values']


class GetInfo:
    """Получение конкретной информации с DataFrame"""

    __lonely = None

    def __new__(cls, *args, **kwargs):
        if cls.__lonely is None:
            cls.__lonely = super().__new__(cls)
        return cls.__lonely

    def __init__(self):
        self.__table = pd.DataFrame(GS().get_spreadsheet_values())

    def get_employees(self):
        # ключ - индекс фамилии значение - фамилия
        emp = self.__table.iloc[4]
        return {emp[i]: i for i in range(len(emp)) if emp[i] not in ('', None)}

    def get_table(self):
        return self.__table


class CreateTable:
    """Транслейт таблиц в датафрейм"""
    month_list = ['', 'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь',
                  'Ноябрь', 'Декабрь']
    __lonely = None
    __table_storage = {}

    def __new__(cls, *args, **kwargs):
        if cls.__lonely is None:
            cls.__lonely = super().__new__(cls)
        return cls.__lonely

    def __init__(self, last_name, month, year):
        self.__last_name = last_name
        self.month = month
        self.year = year
        if self.month + self.year in self.__table_storage:
            self.__table = self.__table_storage[self.month + self.year]
        else:
            self.__table = pd.DataFrame(GS(self.month, self.year).get_spreadsheet_values())
            self.__table_storage.update({self.month + self.year: self.__table})

    def get_employees(self):
        # ключ - индекс фамилии значение - фамилия
        emp = self.__table.iloc[4]
        return {emp[i]: i for i in range(len(emp)) if emp[i] not in ('', None)}

    def get_index(self):
        return self.get_employees()[self.__last_name]

    def get_table(self):
        return self.__table


class PersonalTable(CreateTable):
    """Парсинг таблиц"""

    # столбцы c днем недели, и названием смены
    __col = [0, 1, 2]
    # нунежные строки
    __row = [1, 2, 4]
    # воможное время начала ночной смены
    __night_time = ('20,0', '20,5', '21,0', '21,5', '22,0', '22,5', '23,0', '23,5')
    # память персонлаьных таблиц
    __ptable_storage = {}

    def __init__(self, last_name, month, year):
        super().__init__(last_name, month, year)
        self.__last_name = last_name
        self.__index = self.get_index()

    def get_table(self):
        # создаем персональную таблицу, оставляем необходимое и правим индексы
        if self.month + self.year in self.__ptable_storage:
            return self.__ptable_storage[self.month + self.year]
        __table = super().get_table()
        __personal_table = __table[__table.columns[self.__get_indexes()]]
        __personal_table = __personal_table.dropna(how='all')
        __personal_table = __personal_table.drop(self.__row, axis=0)
        __personal_table.set_index(__personal_table.columns[0], inplace=True)
        __personal_table.index = self.__change_ptable_ind(__personal_table.index)
        self.__ptable_storage.update({self.month + self.year: __personal_table})
        return __personal_table

    @staticmethod
    def __change_ptable_ind(indexes):
        new_indexes = []
        col = 0
        for ind in indexes:
            pre_ind = ind
            if ind != '':
                new_indexes.append(ind)
                pre_ind = ind
            else:
                col += 1
                pre_index = pre_ind + f'.{col}'
                new_indexes.append(pre_index)
        return new_indexes

    def __get_indexes(self):
        return self.__col + [ind for ind in range(self.__index, self.__index + 6)]

    @staticmethod
    def __gen_ind_check(day, indexes):
        ind_check = [day + f'.{str(i)}' for i in range(1, 5)]
        ind_check = [ind for ind in ind_check if ind in indexes]
        ind_check.insert(0, day)
        return ind_check

    def get_work_df(self, day=dt.now().day):
        # если в этот день работает - возвращает DataFrame, если нет - None
        __table = self.get_table()
        days = self.__gen_ind_check(str(day), __table.index)
        for ind in days[::-1]:
            cell = __table.iloc[int(ind)][self.__index]
            if cell != '':
                __work_table = [__table.iloc[int(ind)] for ind in days]
                # если смена ночная и начинается после 20
                if cell in self.__night_time:
                    days = self.__gen_ind_check(str(day + 1), __table.index)
                    __work_table = __work_table + [__table.iloc[int(ind)] for ind in days]
                return pd.DataFrame(__work_table)


class LightPerson(PersonalTable):
    """Обработка графика для конкретного работника"""

    __index_name = ('День:', 'День недели:', 'Наименование смены:', 'Время начала смены:', 'Время окончания смены:',
                    'Время начала перерыва:', 'Время окончания перерыва:', 'Длительность смены:', 'Ночных часов:')
    month_list = ['', 'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь',
                  'Ноябрь', 'Декабрь']

    def __init__(self, last_name, day=dt.now().day, month=dt.now().month, year=dt.now().year):
        self.month = month
        self.year = year
        self.__last_name = last_name
        self.__day = day
        self.__message = {}
        super().__init__(last_name, month, year)

    def __generate_info(self):
        __day_table = self.get_work_df(self.__day)
        __indexes = [ind for ind in range(self.get_index(), self.get_index() + 6)]
        if __day_table is None:
            return 'У вас выходной!'
        work_indexes = [ind for ind in __day_table.index.where(__day_table[self.get_index()] != '') if ind is not None]
        days = [day[:2:] for day in work_indexes if day is not None]
        day_week = [dw for dw in __day_table[1] if dw != '']
        work_name = [wn for wn in __day_table[2].loc[work_indexes] if wn is not None]
        info = self.del_dup([days, day_week, work_name])
        for i in range(6):
            info.append([inf for inf in __day_table[__indexes[i]].loc[work_indexes] if inf is not None])
        return info

    @staticmethod
    def del_dup(data):
        return [list(dict.fromkeys(info)) for info in data]

    def get_message(self, auto=False):
        data = self.__generate_info()
        if len(data) == 15:
            return data
        for i, key in enumerate(self.__index_name, 0):
            self.__message.update({key: data[i]})
        if auto:
            return self.del_dup((self.__message[self.__index_name[2]], self.__message[self.__index_name[3]]))
        return self.redact_message(self.__message)

    @staticmethod
    def redact_message(message: dict):
        def fix_time(time):
            total = 0
            ost = 0
            for t in time:
                total += int(t.split(',')[0])
                ost += int(t.split(',')[1])
            ost = ost // 10 + ost % 10
            return total + ost

        reformat_message = f''
        if len(message['Время начала смены:']) == 1:
            for key, value in message.items():
                value = str(*value)
                reformat_message += f'{key} {value}\n'
            return reformat_message
        else:
            i = 0
            for key, value in message.items():
                if i in (0, 1, 2):
                    value = ', '.join(value)
                    reformat_message += f'{key} {value}\n'
                elif i in (3, 5):
                    reformat_message += f'{key} {value[0]}\n'
                elif i in (4, 6):
                    reformat_message += f'{key} {value[-1]}\n'
                else:
                    reformat_message += f'{key} {fix_time(value)}\n'
                i += 1
            return reformat_message

    def get_month_time(self):
        month = self.month_list[self.month]
        with session as ses:
            work_time = ses.query(WorkTime.time).join(Employee).filter(Employee.last_name == self.__last_name,
                                                                       WorkTime.month_id == self.month).scalar()
            if work_time is None:
                __index = self.get_index() + 4
                __mount_time = self.get_table()
                try:
                    __mount_time = __mount_time[__index].loc['Количество часов:']
                except KeyError:
                    #      используется в том случае, чтобы найти индекс 'Количество часов:' - когда не по стандарту сделан график
                    row = self.__get_row(__mount_time)
                    __mount_time = __mount_time[__index].loc[row]
                id = ses.query(Employee.id).filter(Employee.last_name == self.__last_name)
                to_add = WorkTime(month_id=self.month,
                                  month=self.month_list[self.month],
                                  time=__mount_time,
                                  employee_id=id)
                ses.add(to_add)
                ses.commit()
                return f"<b>Количество отработанных часов за {month}</b>: {self.worktime_check(__mount_time, month)}\n"
            else:
                return f"<b>Количество отработанных часов за {month}</b>: {self.worktime_check(work_time, month)}\n"

    def get_all_time(self):
        with session as ses:
            all_time = ses.query(WorkTime.time).join(Employee).filter(Employee.last_name == self.__last_name).all()
        sum = 0
        ost = 0
        for time in all_time:
            sum += int(time[0].split(',')[0])
            ost += int(time[0].split(',')[1])
        res = sum + (ost // 10)
        res = str(res) + ',' + str(ost % 10)
        return self.__without_month(), self.worktime_check(res, 'За год')

    def __without_month(self):
        with session as ses:
            month_db = ses.query(WorkTime.month).join(Employee).filter(Employee.last_name == self.__last_name).all()
            month_db = [m[0] for m in month_db]
            # мясяцы, которых нет в бд
            not_in_db = set(self.month_list) - set(month_db)
            if len(not_in_db) == 1:
                return None
            not_in_db.remove("")
            no_db = ', '.join(not_in_db)
            p = 0
            return f'\n<b>Не учтенные месяцы: {no_db}\nЕсли не учтенные месяцы присутсвуют в клавиатуре,' \
                   f' пожалуйста нажмите на кнопку не ученного месяца!</b>'

    def worktime_check(self, time, how):
        normal_time = industrial_calendar[dt.now().year][how]
        time = time.replace(',', '.')
        if float(time) - normal_time > 0:
            return f'{time}\nпереработка {float(time) - normal_time} ч.\n'
        elif float(time) - normal_time < 0:
            return f'{time}\nнедоработка {abs(float(time) - normal_time)} ч.\n'
        return time

    @staticmethod
    def __get_row(table):
        for row in table.index[::-1]:
            for val in table.loc[row]:
                if val == 'Количество часов:':
                    return row



