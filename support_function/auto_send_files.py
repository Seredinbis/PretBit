import datetime
import asyncio

from sheets_api.g_sheets import WorkTest
from handlers.fltrs.all_filters import genre_show_f
from bot import bot
from disk_api.yandex_d import FromYandex
from aiogram.types.input_file import URLInputFile
from .delete_file_after import del_files


async def prepare_send(user_name, condition, user_id) -> None:
    while True:
        data = WorkTest(user_name).if_work()
        if condition == 'disable':
            break
        # сколько часов до нулей?
        time_to_zero = 24 - datetime.datetime.now().time().hour
        if type(data[1]) == str:
            # просыпаемся за 2 час до смены
            time = 2
            await asyncio.sleep((int(data[1][:-2:]) - time) * 3600)
            # выводим СЕГОДНЯ
            await bot.send_message(chat_id=user_id,
                                   text=data[0])
            # тут юзаем функцию отправки! и запихиваем сюда какие спектакли надо подгрузить
            await auto_send(data[2], user_id)
            # после этогос спим до нулей
            await asyncio.sleep(time_to_zero*3600)
        else:
            break


async def auto_send(data, user_id) -> None:
    list_doc_id = []
    for spec in data[2]:
        for show in genre_show_f['Опера']:
            if show in spec['Наименование смены'] and 'спектакл' in spec['Наименование смены'].lower():
                files = FromYandex(genre='Опера',
                                   show=show,
                                   what='Паспорт спектакля').get_files()
                if files is None:
                    msg = await bot.send_message(chat_id=user_id,
                                                 text='К сожалению паспорт на этот спектакль отсутсвует,'
                                                      ' скоро это исправится!')
                    await asyncio.sleep(20)
                    await msg.delete()
                else:
                    msg = await bot.send_message(chat_id=user_id,
                                                 text='Идет отправка файлов...')
                    for file in files:
                        url = file['file']
                        name = file['name']
                        document = URLInputFile(url=url,
                                                filename=name)
                        doc_send = await bot.send_document(chat_id=user_id,
                                                           document=document)
                        list_doc_id.append(doc_send.message_id)
                    await msg.delete()
        for show in genre_show_f['Балет']:
            if show in spec['Наименование смены'] and 'спектакл' in spec['Наименование смены'].lower():
                files = FromYandex(genre='Балет',
                                   show=show,
                                   what='Паспорт спектакля').get_files()
                if files is None:
                    msg = await bot.send_message(chat_id=user_id,
                                                 text='К сожалению паспорт на этот спектакль отсутсвует,'
                                                      ' скоро это исправится!')
                    await asyncio.sleep(20)
                    await msg.delete()
                else:
                    msg = await bot.send_message(chat_id=user_id,
                                                 text='Идет отправка файлов...')
                    for file in files:
                        url = file['file']
                        name = file['name']
                        document = URLInputFile(url=url,
                                                filename=name)
                        doc_send = await bot.send_document(chat_id=user_id,
                                                           document=document)
                        list_doc_id.append(doc_send.message_id)
                    await msg.delete()
    await delete_after_5_hourse(chat_id=user_id,
                                list_doc_id=list_doc_id)


async def delete_after_5_hourse(chat_id, list_doc_id) -> None:
    # спим 5 часов
    await asyncio.sleep(3600*5)
    await del_files(chat_id=chat_id,
                    files_list=list_doc_id)
