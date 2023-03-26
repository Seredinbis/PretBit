import apiclient
import httplib2
import datetime
import os
import json

from oauth2client.service_account import ServiceAccountCredentials
from config_data.config import load_config


class LightPerson:
    def __init__(self, sname):
        # тут авторизация в гугл шитс
        # s.name - фамилия человека, передается с обьектом
        # spreadsheet_info - вся инфа о гугл таблице spreadsheet_IDъ
        # ALL_diapozon - весь диапозон ячеек в таблице
        # ALL_values - массив информации из таблицы по спискам, по колоннам
        # column_name - Список порядка вывода информации смены
        # family_index - индекс фамилии
        # day_index - индекс текущего дня
        # col_row_in_day - колличество рядов в дне
        # values_for_name - все значения для фамилии, в текущий день

        # тут узнаем путь к файлу и получаем токен из него
        abspath = os.path.abspath('.env')
        config = load_config(abspath)
        json_token: dict = config.google_sheets_api.token
        google_sheets_token = json.loads(json_token)

        self.sname = sname
        self.spreadsheet_ID = '1iw2mz3md74UeCIMy3eXnfBH-E2-rhwBkWosxwVZVJxM'
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(google_sheets_token,
                                                                       ["https://www.googleapis.com/auth/spreadsheets",
                                                                        "https://www.googleapis.com/auth/drive"])
        httpauth = credentials.authorize(httplib2.Http())
        self.service = apiclient.discovery.build('sheets', 'v4', http=httpauth)
        self.spreadsheet_info = self.service.spreadsheets().get(spreadsheetId=self.spreadsheet_ID).execute()
        self.data = f'{datetime.datetime.now().day}' + '.' + f'{datetime.datetime.now().month}' + '.' + \
                    f'{datetime.datetime.now().year}'
        self.current_list_name = self.get_correct_list_name()
        self.ALL_diapozon = f'{self.get_correct_list_name()}!A1:FC{self.get_amount_rows()}'
        self.ALL_values = self.get_values(diapozon=self.ALL_diapozon)
        self.family_list = {'Глухов': 'Начальник смены',
                            'Быкова': 'Начальник смены',
                            'Касырев': 'Инженер',
                            'Середин': 'Инженер',
                            'Леонов': 'Инженер',
                            'Светухин': 'Техник',
                            'Букач': 'Техник',
                            'Гаршин': 'Осветитель',
                            'Попов': 'Осветитель',
                            'Довгополый': 'Осветитель',
                            'Петухов': 'Осветитель',
                            'Дорошенко': 'Осветитель',
                            'Жуков': 'Осветитель',
                            'Ерусалимский': 'Осветитель',
                            'Вознесенский': 'Осветитель',
                            'Буканов': 'Осветитель',
                            'Мосеев': 'Осветитель',
                            'Лизунова': 'Светооператор',
                            'Яхонтова': 'Светооператор',
                            'Чумичёва': 'Светооператор'}
        self.columns_name = ['День текущего месяца',
                             'Имя дня',
                             'Наименование смены',
                             'Время начала смены',
                             'Время окончания смены',
                             'Время начала перерыва',
                             'Время окончания перерыва',
                             'Кол-во рабочих часов в смене',
                             'Кол-во ночных часов в смене']
        self.month_choose = ['',
                             'Январь',
                             'Февраль',
                             'Март',
                             'Апрель',
                             'Май',
                             'Июнь',
                             'Июль',
                             'Август',
                             'Сентябрь',
                             'Октябрь',
                             'Ноябрь',
                             'Декабрь']
        self.industrial_calendar = {2023: {'Январь': 136,
                                           'Февраль': 143,
                                           'Март': 175,
                                           'Апрель': 160,
                                           'Май': 160,
                                           'Июнь': 168,
                                           'Июль': 168,
                                           'Августь': 184,
                                           'Сентябрь': 168,
                                           'Октябрь': 176,
                                           'Ноябрь': 167,
                                           'Декабрь': 168,
                                           'За год': 1973}}
        self.family_index = self.search_name(self.sname)
        self.col_row_in_day = self.test_col_row_in_day()
        self.values_for_name = self.name_values(self.col_row_in_day, self.index_row(), self.family_index)
        self.day_index_plus = None
        self.data = f'{datetime.datetime.now().day}' + '.' + f'{datetime.datetime.now().month}' + '.' + \
                    f'{datetime.datetime.now().year}'

    def get_correct_list_name(self, month_number=datetime.datetime.now().month) -> str:
        # ищем имя листа текущего месяца, по месяцу и году(по умолчанию)
        # если явно указать moht number - ,будет искать по указанному месяцу
        # print('correct_list_name_search')
        list_name = []
        for rs_i in range(len(self.spreadsheet_info['sheets'])):
            list_name.append(self.spreadsheet_info['sheets'][rs_i]['properties']['title'])
        month_list = ['', 'янв', 'фев', 'мар', 'апр', 'май', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']
        now = datetime.datetime.now()
        for mounth in list_name[::-1]:
            if month_list[month_number] in mounth.lower() and str(now.year)[-2:] in mounth:
                return mounth

    def get_amount_rows(self, list_name=None) -> str:
        # Возвращает количество рядов в листе текущего месяца
        # print('get_amount_rows')
        if list_name is None:
            list_name = self.current_list_name
        else:
            list_name = list_name
        for rs_i in range(len(self.spreadsheet_info['sheets'])):
            # находим нужный лист
            if self.spreadsheet_info['sheets'][rs_i]['properties']['title'] == list_name:
                all_amount_rows = self.spreadsheet_info['sheets'][rs_i]['properties']['gridProperties']['rowCount']
                return all_amount_rows
        print('Ошибка! Нет совпадений!')

    def get_values(self, diapozon) -> dict:
        # Функция дает возможность получить масиив значений по диапозону(номерация ячеек в google sheets)
        # values в json формате
        # print('get_values')
        values = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheet_ID,
                                                          range=diapozon,
                                                          majorDimension='COLUMNS').execute()
        return values

    def search_name(self, s_name) -> int:
        # s-name - фамилия
        # можно улучшить, чтобы диапозон считался самостоятельно????
        # if len(sn_in_all) > 0:  для того, чтобы избежать ошибки пустого списка в следующим if
        # A5:EV5 - шапка, там находятся фамилии! Ищет введеную фамилию в таблице и выводит его индекс
        # возвращает индекс фамилии
        # print('search_name')
        diapozon = f'{self.current_list_name}!A5:EV5'
        index_sn = 0
        for sn_in_all in self.get_values(diapozon)['values']:
            index_sn += 1
            if len(sn_in_all) > 0:
                if s_name in sn_in_all[0]:
                    return index_sn - 1
        print('Ошибка! Ошибка имени!')

    def index_row(self, day=datetime.datetime.now().day) -> int:
        # Возвращает индекс дня
        # return k - 1   -1 потому что индексы считаются с 0, а мы начинаем с 1 костыль ссаный
        # print('index_row')
        k = 0
        for dayy in self.ALL_values['values'][self.columns_name.index('День текущего месяца')]:
            k += 1
            if str(day) == dayy:
                return k - 1

    def create_values_for_name_one_row(self, col_row_in_day, day_index, f_index=None) -> dict:
        # Возвращает словарь рабочего времени и инфлрмации о смене для конкретного имени
        # КОСТЫЛЬ   +4 и +5 в графике нее совпадает ячейка времени смены, с индексом имени
        # создает правильный словарь одного ряда
        # print('get_values_for_name')
        if f_index is None:
            f_index = self.family_index
        row_values = {}
        need_index = (0, 1, 2, 3, 4, 5, 6, f_index + 4, f_index + 5)
        p = 0
        count = 0
        for n_i in need_index:
            for j in self.columns_name[p::]:
                if len(self.ALL_values['values'][n_i]) <= day_index + col_row_in_day:
                    row_values.update({j: ''})
                    count += 1
                    break
                else:
                    row_values.update({j: self.ALL_values['values'][n_i][day_index + col_row_in_day]})
                    p += 1
                    break
        return row_values

    def test_col_row_in_day(self, day_index=None, day_number=datetime.datetime.now().day) -> int:
        # Проверка индекса дня на колв-во рядов
        # break Если в колонке чисел не пустота и не число текущего дня - прерываем цикл
        # return coll_row-2    - 1 потому что последний раз цикла лишний
        # print('test_col_row_in_day')
        if day_index is None:
            day_index = self.index_row()
        coll_row = 0
        for coll_row in range(8):  # 8 потому что не бывает у нас больше 6 рядов в день, до 8 на всякий
            if self.ALL_values['values'][2][day_index + coll_row] != '' or \
                    self.ALL_values['values'][0][day_index + coll_row] == str(day_number):
                pass
            else:
                break
        return coll_row - 1

    def name_values(self, col_row_in_day, day_index, f_index=None) -> [dict]:
        # Создаем список рядов в дне, тут все значения для введенной фамилии, в текущий день
        # print('values_for_name')
        vals_for_name = []
        for how_row_in_day in range(col_row_in_day + 1):
            vals_for_name.append(self.create_values_for_name_one_row(how_row_in_day, day_index, f_index))
        return vals_for_name


class SickTest(LightPerson):
    def generate_table_col_index(self, sick_day_plus=0, day_index=None) -> str:
        # Уравнение присваивания индекса колонки
        # print('generate_table_col_index')
        # 25 ,erd
        if day_index is None:
            day_index = self.index_row()
        list_column_word = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                            'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
                            'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        # если индекс фапмилии меньше или равно количеству цифр - присваимваем букву, иначе нужно 2 буквы
        if len(list_column_word) >= self.family_index + 4:
            for n_word in range(len(list_column_word)):
                if n_word == self.family_index + 4:
                    column_word = list_column_word[n_word]
                    return self.current_list_name + '!' + column_word + str(day_index + 1 + sick_day_plus)
        else:
            index = 25
            # тут делаем 2 буквы
            for word in list_column_word:
                for word_2 in list_column_word:
                    # +1 КОСТЫЛЬ
                    index += 1
                    if index == self.family_index + 4:
                        column_word = word + word_2
                        return self.current_list_name + '!' + column_word + str(day_index + 1 + sick_day_plus)

    def sick_day_test(self, sick_day_plus=0, day_index=None) -> bool:
        # Проверка цвета ячейки на больничный
        # print('sick_day_test')
        word_index_info = self.service.spreadsheets().get(spreadsheetId=self.spreadsheet_ID,
                                                          ranges=self.generate_table_col_index(sick_day_plus,
                                                                                               day_index),
                                                          includeGridData=True).execute()
        color = word_index_info['sheets'][0]['data'][0]['rowData'][0]['values'][0]['effectiveFormat']['backgroundColor']
        if color == {'red': 1, 'green': 1}:
            return True
        else:
            return False

    def sick_day_range(self) -> str:
        # Вывод диапозона дней больничного
        # print('sick_day_range')
        sick_day_plus = 0
        day_index = self.index_row()
        while True:
            if self.sick_day_test(sick_day_plus):
                sick_day_plus += 1
            else:
                # +1 потому что в новом дне у нас сначало идет путсой ряд
                last_day = self.create_values_for_name_one_row(col_row_in_day=sick_day_plus + 1,
                                                               day_index=day_index)['День текущего месяца']
                return f'<b>У вас больничный по {last_day} число, включительно.</b>'

    def if_sick(self) -> str:
        # если больничный - возвращает о нем инофрмацию
        # print('if_sick')
        if self.sick_day_test():
            for work in self.values_for_name:
                if work['Наименование смены'] != 'ВЫХОДНОЙ':
                    return f'{self.sick_day_range()} Пожалуйста, больше отдыхайте и выздоравливайте, ждем вас' \
                           f' готовым войти в раблочий режим! Сегодня {self.data} рабочая смена!'
                elif work['Наименование смены'] == 'ВЫХОДНОЙ':
                    return f'{self.sick_day_range()} Пожалуйста, больше отдыхайте и выздоравливайте, ждем вас' \
                           f' готовым войти в раблочий режим! Сегодня у осветительской службы выходной!'


# требуется тестирование данного класса
class NightWorkTest(LightPerson):
    def night_work_test(self) -> bool:
        # Проверка ночной смены
        # В этом иф проверяем наличие ночной смены в текущем и следующем дне и наличие в этих сменах рабочих часов!
        # для текущего дня values_for_name
        # для следующего нужен новый запрос, так как в values_for_name только текущий день
        # [::3]  чтобы осталась только целая часть
        # day_index + 2 - чтобы перепрыгнуть на 1 ряд следющего дня, тк +1 это пустота между днями
        # print('night_work_test')
        day_index = self.index_row()
        self.day_index_plus = 0
        if 'Кол-во рабочих часов в смене' in self.values_for_name[-1]:
            if int(self.values_for_name[-1]['Время начала смены'][:-2:]) >= 21:
                if self.values_for_name[-1]['Кол-во рабочих часов в смене'] != '':
                    self.day_index_plus = 0
                    return True
        # print(self.create_values_for_name_one_row(self.col_row_in_day,
        #                                              self.day_index + 2)['Время начала смены'][:-2:])
        elif self.create_values_for_name_one_row(self.col_row_in_day,
                                                 day_index + 2)['Наименование смены'] == 'ВЫХОДНОЙ':
            return False
        elif self.create_values_for_name_one_row(self.col_row_in_day,
                                                 day_index + 2)['Кол-во рабочих часов в смене'] != '':
            if int(self.create_values_for_name_one_row(self.col_row_in_day,
                                                       day_index + 2)['Время окончания смены'][:-2:]) < 12:
                if int(self.create_values_for_name_one_row(self.col_row_in_day,
                                                           day_index + 2)['Время начала смены'][:-2:]) >= 0:
                    self.day_index_plus = 2
                    return True
        else:
            return False

    def if_night(self) -> tuple:
        # если есть ночная смена - возвращает о ней информацию
        # print('if_night')
        if self.night_work_test():
            work = self.create_values_for_name_one_row(self.col_row_in_day,
                                                       self.index_row() + self.day_index_plus)
            return f'<b>У Вас сегодня ночная смена!</b> ' \
                   f'{work["Наименование смены"]}.\n Cмена длится с {work}["Время начала смены"] до' \
                   f'{work}["Время окончания смены"].\n' \
                   f' </b>Продолжительность смены:</b> {work}["Кол-во рабочих часов в смене"]', \
                work['Время начала смены'], \
                work


class WorkTest(LightPerson):
    def if_work(self) -> tuple:
        # выводит, что у нас сегодня, если в дне 1 ряд
        # если в дне больше рядов, чем 1
        # print('if_work')
        #
        if len(self.sort_work_row()) != 0:
            work_time = self.get_work_time(self.sort_work_row())
        else:
            work_time = self.get_work_time(self.values_for_name)
        if len(self.sort_work_row()) == 1:
            # цикл, чтобы достать словарь из списка
            # нужно ли денлать tuple?????
            for work in self.sort_work_row():
                return f'<b>У Вас сегодня рабочий день!</b>\nСегодня в театре:\n' \
                       f'{self.get_who_working(quests=self.sort_work_row())}\n' \
                       f'<b>Продолжительность рабочего дня:</b> с {work_time[0]} до {work_time[1]}.' \
                       f'\n{self.get_pause(work)}', work_time[0], self.sort_work_row()
        elif len(self.sort_work_row()) > 1:
            return self.ged()
        else:
            return f'<b>У Вас сегодня выходной, набирайтесь сил!</b>\nСегодня в театре:\n' \
                   f'{self.get_who_working(quests=self.values_for_name)}\n<b>Продолжительность рабочего дня:</b> с' \
                   f' {work_time[0]} до {work_time[1]}.\n{self.get_pause(self.values_for_name)}', False

    def sort_work_row(self) -> list:
        # если в дне более 1 ряда - это функция обрабатывает список словарей с рядами и возвращает список рабочих дней!
        # ворзвращает список словарей, только те словари, где проставлены количесвто рабочих часов
        # print('sort_work_row')
        work_phase = []
        # сортируем список, теперь в work_phase, только рабочие ряды дня!
        for values in self.values_for_name:
            if values['Кол-во рабочих часов в смене'] != '':
                work_phase.append(values)
        return work_phase

    # тут необходимо тестирование!
    def get_who_working(self, quests, day_ind=None) -> str:
        # day_index - используется, если вызывается функция через КАЛЕНДАРЬ
        # data_for_calendar - так же для КАЛЕНДАРЬ, чтобы забирать от туда все фамилии, которые работают
        # val_f_name - тут используем для того, чтобы выбрать данные с дня - day_ind, это либо текущий, либо с календаря
        result = 'Квесты:\n'
        if day_ind is None:
            day_ind = self.index_row()
        data_for_calendar = self.ALL_values['values']
        data_work = self.sort_work_row()
        who_list = []
        quest = self.get_col_quest(quests).split('\n')[1::]
        col_row = self.test_col_row_in_day(day_index=day_ind)
        val_f_name = self.name_values(col_row, day_ind, self.family_index)
        equals_index = self.how_index_equals(quests, val_f_name)
        # тут бегаем по общему графику и выводим в who_list - кто сегодня работает,
        for index_plus in range(len(val_f_name)):
            who_str = ''
            for ind in range(len(data_for_calendar)):
                if len(data_for_calendar[ind]) >= day_ind + index_plus:
                    if len(data_for_calendar[ind][4]) > 3:
                        if data_for_calendar[ind][4].split(' ')[0] in self.family_list:
                            if data_for_calendar[ind + 4][day_ind + index_plus] != '':
                                # если у человека больничный - добавляем ему в скобочках(на больничном)
                                # этот кусок кода не можети быть исопльзован, так как с постоянными запросами
                                # сервер крашиться, превышается допкстимое количесво запросов
                                # print(SickTest(data_for_calendar[ind][4].split(' ')[0]).
                                # sick_day_test(day_index=day_ind))
                                # if SickTest(data_for_calendar[ind][4].split(' ')[0]).sick_day_test(day_index=day_ind):
                                #     print(day_ind)
                                # print(data_for_calendar[ind][4].split(' ')[0])
                                # print('VOT ONO')
                                # who_str += data_for_calendar[ind][4].split(' ')[0] + '(на больничном)' + ', '
                                # else:
                                who_str += data_for_calendar[ind][4].split(' ')[0] + ', '
            who_list.append(who_str[:-2:])
        if val_f_name == quests:
            for index_pluss in range(len(val_f_name)):
                result += f'{quest[index_pluss]}\n<b>Количество работников на смене:</b>' \
                          f' {who_list[index_pluss].count(",") + 1}\n' \
                          f'<b>Cостав смены:</b> {who_list[index_pluss]}\n\n'
        elif quests == data_work:
            for index_pluss in range(len(data_work)):
                for index in equals_index:
                    result += f'{quest[index_pluss]}\n<b>Количество работников на смене:</b>' \
                              f'{who_list[index].count(",") + 1}\n' \
                              f'<b>Cостав смены:</b> {who_list[index]}\n\n'
                    equals_index.pop(0)
                    break
        return result

    @staticmethod
    def get_col_quest(quests) -> str:
        # подсчет квестов, и их корректный вывод
        # print('get_col_quest')
        quest_list = []
        counter = 1
        vid = ''
        if type(quests) == list:
            for quest in quests:
                quest_list.append(quest['Наименование смены'])
        else:
            quest_list.append(quests['Наименование смены'])
        for que in quest_list:
            vid += f'<b>{counter}</b>: {que}\n'
            counter += 1
        return f'<b>Квесты:</b>\n' + vid

    @staticmethod
    def get_work_time(quests) -> list:
        # возвращает времяначала и конца рабочего дня, в зависимости от кол-ва рабочих квестов
        # print('get_work_time')
        if quests[-1]['Время окончания смены'] != '24,0':
            return [quests[0]['Время начала смены'], quests[-1]['Время окончания смены']]
        else:
            return [quests[0]['Время начала смены'], quests[-2]['Время окончания смены']]

    @staticmethod
    def get_pause(quests) -> str:
        # возвращает строку с временем перерывов, в зависимости от кол-ва квестов
        # print('get_pause')
        start_pause_list = []
        end_pause_list = []
        counter_pause = 0
        counter = 1
        vid = ''
        if type(quests) == list:
            for pause in quests:
                if pause['Время начала перерыва'] != '':
                    counter_pause += 1
                    start_pause_list.append(pause['Время начала перерыва'])
                    end_pause_list.append(pause['Время окончания перерыва'])
        else:
            counter_pause += 1
            start_pause_list.append(quests['Время начала перерыва'])
            end_pause_list.append(quests['Время окончания перерыва'])
        if len(start_pause_list) == 0 or len(end_pause_list) == 0:
            return '<b>У Вас сегодня нет перерыва, по графику</b>.'
        else:
            for time in range(len(start_pause_list)):
                vid += f'<b>Перерыв {counter}:</b> с {start_pause_list[time]} до {end_pause_list[time]}\n '
                counter += 1
            return f'Кол-во перерывов: {counter_pause}.\n ' + vid

    def ged(self) -> tuple:
        # функция подготовки вывода информации про рабочий день, если в смене рабочих рядов больше 1
        # print('ged')
        work = self.sort_work_row()
        work_time = self.get_work_time(work)
        return f'<b>У Вас сегодня рабочий день!</b>\n' \
               f'{self.get_who_working(quests=work)}\n' \
               f'<b>Продолжительность рабочего дня</b>: с {work_time[0]} до {work_time[1]}.\n{self.get_pause(work)}', \
            work_time[0], self.sort_work_row()

    @staticmethod
    def how_index_equals(quests, val_f_name) -> list:
        # функция помогает правильно составить чтото
        # print('how_index_equals')
        index_list = []
        for i in val_f_name:
            for j in quests:
                if i == j:
                    index_list.append(val_f_name.index(j))
        # print(index_list)
        return index_list

    #     ДАЛЕЕ ИДУТ ФУНКЦИИ СВЯЗАННЫЕ С КНОПКАМИ В БОТЕ


class BotButton(WorkTest):
    def for_calendar_button(self, day_number):
        # print('for_calendar_button')
        ind = self.index_row(day_number)
        col_r = self.test_col_row_in_day(day_index=ind, day_number=day_number)
        fam_ind = self.search_name(self.sname)
        val = self.name_values(col_r, ind, fam_ind)
        return self.work_or_for_calendar(val, ind, day_number)

    def work_or_for_calendar(self, data, index, day_number) -> str:
        # print('work_or_for_calendar')
        month = datetime.datetime.now().month
        year = datetime.datetime.now().year
        work = ''
        work_time_clock = self.get_work_time(data)
        for work_time in data:
            if work_time['Наименование смены'] == 'Выходной':
                return f'В этот, {work_time["День текущего месяца"]}.{month}.{year}, день <b>ОБЩИЙ ВЫХОДНОЙ!</b>'
            if work_time['Кол-во рабочих часов в смене'] != '':
                if (0 <= int(work_time['Время начала смены'][::3]) <= 5) or \
                        int(work_time['Время окончания смены'][:2:]) == 24:
                    work = f'<b>У вас в этот день, {day_number}.{month}.{year},' \
                           f' ночная смена!</b>\n'
                    break
                else:
                    work = f'<b>В этот день, {day_number}.{month}.{year}, вы работаете!</b>\n'
                    break
            else:
                work = f'<b>В этот день, {day_number}.{month}.{year}, у вас выходной!</b>\n'
        return f'{work}\nА в театре:\n' \
               f'{self.get_who_working(quests=data, day_ind=index)}\n' \
               f'<b>Продолжительность рабочего дня с</b>: {work_time_clock[0]} до' \
               f' {work_time_clock[1]}\n{self.get_pause(data)}'

    def get_work_hours_for_month(self, month) -> str:
        # тут ищем данные фамилии по конкретному месяцу
        # в all_values['values'][self.family_index+4]), в -1 и -2 хранятся кол-во часов в месяц, для фамилии
        # -1 это ночные часы из общего кол-ва    -2 общее кол-во часво
        list_name = self.get_correct_list_name(self.month_choose.index(month))
        if list_name is None:
            return f'К сожалению этого месяца еще нет в графике! Поробуйте выбрать другой месяц.'
        else:
            all_diapozon = f'{list_name}!A1:FC{self.get_amount_rows(list_name)}'
            all_values = self.get_values(diapozon=all_diapozon)
            your_hour = int(all_values['values'][self.family_index + 4][-2][:-2:])
            norma_hour = self.industrial_calendar[datetime.datetime.now().year][month]
            return f"<b>Количество отработанных часов за {month}</b>: {your_hour}\n" \
                   f"<b>Норма часов за {month}</b>: {norma_hour}\n" \
                   f"<b>Ваша {self.perenedo_rabotka_for_month(your_hour, norma_hour)}" \
                   f" за {month}</b>: {your_hour - norma_hour}"

    def get_all_work_hours(self) -> str:
        correct_or = []
        all_work_hourse = 0
        ostatok = 0
        rabotka = 0
        year = datetime.datetime.now().year
        for month_number in range(1, 13):
            list_name = self.get_correct_list_name(month_number)
            if list_name is not None:
                correct_or.append(month_number)
                all_diapozon = f'{list_name}!A1:FC{self.get_amount_rows(list_name)}'
                all_values = self.get_values(diapozon=all_diapozon)
                shet_chasov = all_values['values'][self.family_index + 4]
                all_work_hourse += int(shet_chasov[-2][:-2:])
                ostatok += int(shet_chasov[-2][-1])
                rabotka += int(shet_chasov[-2][:-2:]) + int(shet_chasov[-2][-1]) - \
                           self.industrial_calendar[year][self.month_choose[month_number]]
        if self.correct_month_number_or(correct_or) is False:
            return f'ВОЗМОЖНО НЕККОРЕКТНО! ОТСУТСТВУЕТ КАКОЙ-ТО МЕСЯЦ'
        else:
            return f'<b>Количество отработанных часов за {year} год</b>: {all_work_hourse + ostatok / 10}\n' \
                   f'<b>Норма часов за {year} год</b>: {self.industrial_calendar[year]["За год"]}\n' \
                   f'Осталось отработать ' \
                   f'{self.industrial_calendar[year]["За год"] - all_work_hourse + ostatok / 10} часа\n' \
                   f'За последние месяцы(к которым был составлен график) у вас ' \
                   f'{self.perenedo_rabotka_all(rabotka)} в <b>{rabotka}</b> час(a)(ов)'

    @staticmethod
    def correct_month_number_or(correct_or) -> int:
        # тут проверяем все ли цифры идут по порядку в +1 в листе номеров месяцев
        count = 1
        for number in correct_or:
            if count != number:
                return False
            count += 1

    @staticmethod
    def perenedo_rabotka_for_month(your_time, normal) -> str:
        if your_time > normal:
            return 'переработка'
        else:
            return 'недоработка'

    @staticmethod
    def perenedo_rabotka_all(your_time) -> str:
        if your_time > 0:
            return 'переработка'
        else:
            return 'недоработка'


class ResultPrint(LightPerson):
    def today_button(self) -> (tuple, str):
        if SickTest(self.sname).if_sick() is not None:
            return SickTest(self.sname).if_sick()
        elif NightWorkTest(self.sname).if_night() is not None:
            return NightWorkTest(self.sname).if_night()
        else:
            return WorkTest(self.sname).if_work()

    def list_of_employees(self) -> list:
        list_of_employess = []
        for i in self.ALL_values['values']:
            if len(i) < 1:
                continue
            elif len(i[4]) > 4:
                list_of_employess.append(i[4].split(' ')[0])
        return list_of_employess

# a = LightPerson('Середин')
# print(a.get_correct_list_name())
# print()
# print(a.test_col_row_in_day())
# print()
# print(a.index_row())
# print()
# print(a.get_amount_rows())
# print()
# print(a.get_values(f'{a.get_correct_list_name()}!A1:FC{a.get_amount_rows()}'))
# print()
# print(a.create_values_for_name_one_row(a.test_col_row_in_day(), a.index_row()))
# print()
# print(a.name_values(a.test_col_row_in_day(), a.index_row()))
# b = SickTest('Глухов')
# print(b.if_sick())
# c =  NightWorkTest('Леонов')
# print(c.if_night())
# d = WorkTest('Середин')
# print('if work')
# print(d.if_work())
# print()
# print('sort_work_row')
# print(d.sort_work_row())
# print()
# print('get who working')
# print(d.get_who_working(d.sort_work_row()))
# print()
# print('get col quest')
# print(d.get_col_quest(d.sort_work_row()))
# print()
# print('get work time')
# print(d.get_work_time(d.sort_work_row()))
# print()
# print('get pause')
# print(d.get_pause(d.sort_work_row()))
# print()
# print('ged')
# print(d.ged())
# print()
# e = BotButton('Середин')
# print(e.for_calendar_button(15))
# f = ResultPrint('Середин')
# print(f.today_button())
# print(f.list_of_employees())
