import datetime

import apiclient
import httplib2
import os
import json

from oauth2client.service_account import ServiceAccountCredentials
from config_data.config import load_config


class GS:
    def __init__(self, day=None, month=None, family=None):
        print('init')
        # тут узнаем путь к файлу и получаем токен из него
        abspath = os.path.abspath('.env')
        config = load_config(abspath)
        json_token: dict = config.google_sheets_api.token
        google_sheets_token = json.loads(json_token)
        self.spreadsheet_ID = '1iw2mz3md74UeCIMy3eXnfBH-E2-rhwBkWosxwVZVJxM'
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(google_sheets_token,
                                                                       ["https://www.googleapis.com/auth/spreadsheets",
                                                                        "https://www.googleapis.com/auth/drive"])
        httpauth = credentials.authorize(httplib2.Http())
        self.service = apiclient.discovery.build('sheets', 'v4', http=httpauth)
        self.spreadsheet_info = self.service.spreadsheets().get(spreadsheetId=self.spreadsheet_ID).execute()
        if day is None:
            self.today = str(datetime.datetime.now().day)
        else:
            self.today = str(day)
        if family is None:
            self.family = 'Середин'
        else:
            self.family = family
        if month is None:
            self.month = datetime.datetime.now().month
        else:
            self.month = int(month)
        self.get_correct_list_name = self.get_correct_list_namef()
        self.get_amount_rows = self.get_amount_rowsf()
        self.values_rows = self.values_rowsf()
        self.values_columns = self.values_columnsf()
        self.day_indices = self.search_day_indices()
        self.family_values = self.search_family_list()
        self.columns_name = ['День текущего месяца',
                             'Имя дня',
                             'Наименование смены',
                             'Время начала смены',
                             'Время окончания смены',
                             'Время начала перерыва',
                             'Время окончания перерыва',
                             'Кол-во рабочих часов в смене',
                             'Кол-во ночных часов в смене']
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

    def values_columnsf(self, list_name=None):
        print('values_columns')
        # функция возвращает значения всех колонок в табллице - колонка = список
        # get_amount_rows не меняем, чтобы не траить лишнии ресурсы - он всегда примерно одинаковое кол-во
        if list_name is None:
            list_name = self.get_correct_list_name
        return self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheet_ID,
                                                        range=f'{list_name}!A1:FC'
                                                              f'{self.get_amount_rows}',
                                                        majorDimension='COLUMNS').execute()['values']

    def values_rowsf(self):
        print('values_rows')
        # функция возвращает значения всех рядов в таблице - ряд = список
        return self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheet_ID,
                                                        range=f'{self.get_correct_list_name}!A1:FC'
                                                              f'{self.get_amount_rows}',
                                                        majorDimension='ROWS').execute()['values']

    def get_correct_list_namef(self, month=None) -> str:
        # универсальная функция, можно использовать независимо
        # ищем имя листа текущего месяца, по месяцу и году(по умолчанию)
        # если явно указать moht number - ,будет искать по указанному месяцу
        if month is None:
            month = self.month
        print('get_correct_list_name')
        list_name = []
        for rs_i in range(len(self.spreadsheet_info['sheets'])):
            list_name.append(self.spreadsheet_info['sheets'][rs_i]['properties']['title'])
        month_list = ['', 'янв', 'фев', 'мар', 'апр', 'май', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']
        now = datetime.datetime.now()
        for mounth in list_name[::-1]:
            if month_list[month] in mounth.lower() and str(now.year)[-2:] in mounth:
                return mounth

    def get_amount_rowsf(self, list_name=None) -> str:
        # Возвращает количество рядов в листе текущего месяца
        print('get_amount_rows')
        if list_name is None:
            list_name = self.get_correct_list_name
        else:
            list_name = list_name
        for rs_i in range(len(self.spreadsheet_info['sheets'])):
            # находим нужный лист
            if self.spreadsheet_info['sheets'][rs_i]['properties']['title'] == list_name:
                all_amount_rows = self.spreadsheet_info['sheets'][rs_i]['properties']['gridProperties']['rowCount']
                return all_amount_rows
        print('Ошибка! Нет совпадений!')

    def search_family_list(self, val_col=None):
        print('search_family_list')
        if val_col is None:
            val_col = self.values_columns
        family_lists = []
        flag = False
        # функция возвращает список с часами конкретной фамилии записанной в self.family
        for in_list in val_col:
            if in_list == val_col[0] or \
                    in_list == val_col[1] or \
                    in_list == val_col[2]:
                family_lists.append(in_list)
            for item in in_list:
                if self.family in item:
                    flag = True
                    break
            if in_list != [] and flag:
                family_lists.append(in_list)
            elif in_list == [] and flag:
                break
        return family_lists

    def search_day_indices(self):
        print('search_day_indices')
        # функция фозвращает сколько индексов(строк) в рабочем дне
        # ДЛЯ ТЕКУЩЕГО ДНЯ
        for day_index in range(len(self.values_columns)):
            if self.today in self.values_columns[day_index]:
                day_indices = [self.values_columns[day_index].index(self.today)]
                index = self.values_columns[day_index].index(self.today)
                # счетчик n нужен для того, чтобы правильно отсеять другие пустые строки, т.к весь список в них, при
                # поиске индекса выдает нулевой индекс
                n = 1

                for values in self.values_columns[day_index][index + n::]:
                    if values == '':
                        day_indices.append(index + n)
                        n = n + 1
                    else:
                        return day_indices

    def today_data(self):
        print('today_data')
        today_dict = {}
        n = 0
        for data_list in self.values_columns:
            quests = []
            if not data_list:
                return today_dict
            for ind in self.day_indices:
                # исключаем пустые сроки
                if data_list[ind] == '':
                    pass
                else:
                    quests.append(data_list[ind])
                # print(f'{self.columns_name[n]} : {data_list[ind]}')
            today_dict.update({self.columns_name[n]: quests})
            n += 1

    def generate_work_dict(self, day_inds=None):
        # данная функция отделилась от today_data_work, чтобы быть универсальнее
        print('generate_work_dict')
        if day_inds is None:
            day_inds = self.day_indices
        # в этой части кода сортируем нужные индексы(строки, в которых стоят рабочие часы)
        # если кол-во строк отличаются больше, чем на одну - значит меньший индекс не используем!
        dict_by_sort_ind = {}
        # Убираем последний индекс, так как он отсносится к полоске в таьлице(между днями)
        for ind in day_inds[:-1:]:
            ch_by_sort = 0
            for data_list in self.family_values:
                if data_list[ind] != '':
                    ch_by_sort += 1
            if ind == day_inds[0]:
                # убавляем у счетчика номер дня и имя дня
                ch_by_sort = ch_by_sort - 2
            dict_by_sort_ind.update({ind: ch_by_sort})
        # тут(выше) подсчитали, сколько позиций в индексах
        # ниже начяинаем сравнивание и отказываемся от лишних индексов
        keys_when_work = [key for key in dict_by_sort_ind.keys() if dict_by_sort_ind[key] > 1]
        # оставили индексы, у которых больше 1 позиции, такие сейчас являются рабочими сменами!
        # создаем шапку итого словаря, с числом и именем дня
        main_work_dict = {self.columns_name[0]: [self.family_values[0][day_inds[0]]],
                          self.columns_name[1]: [self.family_values[1][day_inds[0]]]}
        # шапка готова, теперь убираем ненужные детали, которые уже готовы и начинаем беготню по спискам,
        # с помощью отсортированных индексов
        # так же сождаем список для обновления словаря
        y = 2
        for data in self.family_values[2::]:
            list_total = []
            for positions in self.columns_name[y::]:
                for index in keys_when_work:
                    list_total.append(data[index])
                main_work_dict.update({positions: list_total})
                y += 1
                break
        return main_work_dict

    def today_data_work(self):
        print('today_data_work')
        # далее пробежимся по созданному словарю, чтобы проверить наличие в нем ночных смен, если ночная смена
        # находится - проверяем первый индекс следующего дня и суммируем их
        # self.day_indices[-1] + 2] - для того чтобы отфильтровать -1 элемент
        main_work_dict = self.generate_work_dict()
        if '24,0' in main_work_dict['Время окончания смены']:
            next_day_night_ind = [self.day_indices[-1] + 1, self.day_indices[-1] + 2]
            # создаеем словарь следующего дня
            half_dict = self.generate_work_dict(day_inds=next_day_night_ind)
            # мерджим словари
            main_work_dict.update({key: main_work_dict.get(key, []) + half_dict.get(key, []) for key in half_dict})
        # проверяем, не выходной ли часом сегодня
        if len(main_work_dict) >= 1:
            for hours in main_work_dict['Кол-во рабочих часов в смене']:
                # если есть что-то кроме '' - не выходной
                if hours != '':
                    return self.correct_output(main_work_dict)
        # если там не вышло - значит нет часов - значит выходной
        return self.correct_output(self.today_data())



    def correct_output(self, data):
        print('correct_output')
        # будем составлять строку, с окончательным выводом данных для бота, переводя словарь в строку
        # определяем список позиций для вывода
        positions = ['Наименование смены', 'Время начала смены', 'Время окончания смены',
                     'Кол-во рабочих часов в смене']
        # тут определяем, сегодня ли это?
        if self.today == str(datetime.datetime.now().month):
            date = f'сегодня, {self.today}.{datetime.datetime.now().month}.{datetime.datetime.now().year}'
        else:
            date = f'{self.today}.{str(datetime.datetime.now().month)}.{datetime.datetime.now().year}'
        # для начала отсеим ночные смены
        if data['Наименование смены'] == ['ВЫХОДНОЙ']:
            return f'У Осветительской службы {date} ВЫХОДНОЙ!', None, None
        elif len(data['День текущего месяца']) > 1:
            output = f'<b>У Вас {date} ночная смена!</b>\n\n'
        # отсеиваем, все, что после запятой у времени
        # если смена начинаться от 0 до 3 - знаяит ночная смена
        elif 3 >= int(data['Время начала смены'][0].split(',')[0]) >= 0:
            output = f'<b>У Вас {date} ночная смена!</b>\n\n'
        elif 21 <= int(data['Время начала смены'][0].split(',')[0]) <= 24:
            output = f'<b>У Вас {date} ночная смена!</b>\n\n'
        # теперь отсеиваем дневные смены, универально, учитывая, сколько квестов в дне
        # если смена начинаеться с 5 до 19 - значит она дневная
        else:
            if 'Кол-во рабочих часов в смене' in data:
                output = f'<b>У Вас {date} рабочая смена!</b>\n\n'
            else:
                output = f'<b>У Вас {date} выходной! А в театре:</b>\n\n'
        # q_ch - счетчик квестов
        # out_comp - строка предварительного вывода
        # составляем окончательный вывод
        out_comp = ''
        # cgписок наименования квестов в этом рабочем дне
        work_quests_list = []
        for q_ch in range(len(data['Время начала смены'])):
            for quest in data:
                if quest in positions:
                    for pos in positions:
                        if pos == 'Наименование смены':
                            out_comp += f'{q_ch + 1} Квест: {data[pos][q_ch]}.\n'
                            work_quests_list.append(data[pos][q_ch])
                        elif pos == 'Время начала смены':
                            out_comp += f'Cмена длится с {data[pos][q_ch]} до '
                            start = int(data[pos][q_ch].split(',')[0])
                            if q_ch == 0:
                                work_hour_start = data[pos][q_ch]
                        elif pos == 'Время окончания смены':
                            out_comp += f'{data[pos][q_ch]}.\n'
                            end = int(data[pos][q_ch].split(',')[0])
                        # в today_data нет кол-ва рабочих часов, только информация о смене
                        if pos in data:
                            if pos == 'Кол-во рабочих часов в смене':
                                out_comp += f'<b>Продолжительность смены:</b> {data[pos][q_ch]}.\n'
                                w_hour = int(data[pos][q_ch].split(',')[0])
                    if 'Кол-во рабочих часов в смене' in data:
                        out_comp += f'Продолжительность обеда: {end - start - w_hour} час(а, ов).\n\n'
                    break
        return output + out_comp, work_hour_start, work_quests_list

    @staticmethod
    def perenedo_rabotka_for_month(your_time, normal, month) -> str:
        if your_time > normal:
            return f'переработка за {month}</b>: {your_time - normal}'
        else:
            return f'недоработка за {month}</b>: {abs(normal - your_time)}'

    @staticmethod
    def perenedo_rabotka_all(your_time) -> str:
        if your_time > 0:
            return 'переработка'
        else:
            return 'недоработка'

    def work_hour_mounth(self):
        # функция возвращает количесво отработанных часво в месяц + недорапботки и переработки
        month = self.get_correct_list_name
        for m in self.month_choose:
            if m in month and m != '':
                month = m
                break
        print(month)
        month_hours = float(self.family_values[self.columns_name.index('Кол-во рабочих часов в смене')]
                            [-2].replace(',', '.'))
        norma_hour = float(self.industrial_calendar[datetime.datetime.now().year][month])
        return f"<b>Количество отработанных часов за {month}</b>: {month_hours}\n" \
               f"<b>Норма часов за {month}</b>: {norma_hour}\n" \
               f"<b>Ваша {self.perenedo_rabotka_for_month(month_hours, norma_hour, month)}"

    def work_hour_all(self):
        # функция бегает по листам, с определенным именем и вытаскивает, с каждого листа, кол-во отработонного
        # времени в месяц
        year = datetime.datetime.now().year
        total_hour = 0
        total_norm_hour = 0
        for month in self.month_choose:
            corr_ln = self.get_correct_list_namef(month=self.month_choose.index(month))
            print(corr_ln)
            if corr_ln is not None and month != '':
                val_col = self.values_columnsf(list_name=corr_ln)
                fam_val = self.search_family_list(val_col=val_col)
                if len(fam_val) > 3:
                    total_hour += float(fam_val[self.columns_name.index('Кол-во рабочих часов в смене')]
                                [-2].replace(',', '.'))
                    total_norm_hour += self.industrial_calendar[year][month]
        return f'<b>Количество отработанных часов за {year} год</b>: {total_hour}\n' \
               f'<b>Норма часов за {year} год</b>: {self.industrial_calendar[year]["За год"]}\n' \
               f' За последние месяцы(к которым был составлен график) у вас' \
               f' {self.perenedo_rabotka_all(total_hour-total_norm_hour)}' \
               f' в <b>{abs(total_hour-total_norm_hour)}</b> час(a)(ов)'

    def list_of_employees(self):
        # функция для вывода всех фамилий в графике
        # можно начинать с 8 индекса, там начинаются фамилии работников
        # каждый 6 список - пустой
        employees = []
        for data in self.values_columns[8::]:
            if data:
                if len(data[4]) > 4:
                    employees.append(data[4].split(' ')[0])
        return employees


gs = GS(family='Мосеев')
print(gs.today_data_work())
print(gs.work_hour_all())