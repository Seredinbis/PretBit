import datetime
import asyncio
import logging

from sheets_api.gs import GS
from handlers.fltrs.all_filters import genre_show_f
from bot import bot, for_delete
from disk_api.yandex_d import FromYandex
from aiogram.types.input_file import URLInputFile

# блок настройки логирования
# устанавливаем имя и уровень
logger_as = logging.getLogger(__name__)
logger_as.setLevel(logging.INFO)
# настраиваем обработчик и форматор
handler_as = logging.FileHandler(f"{__name__}.log", mode='w')
formater_as = logging.Formatter('%(name)s %(asctime)s %(levelname)s %(message)s')
# добавляем форматировщик к обработчику
handler_as.setFormatter(formater_as)
# добавляем обработчик к логеру
logger_as.addHandler(handler_as)


async def time_to_zero() -> int:
    # блок кода вычисляющий время до нулей
    now = datetime.datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    delta = midnight - now
    time_to_zero = delta.total_seconds()
    # убираем все после запятой и переводим в положительное число, изначательно со знаком минус
    return abs(int(time_to_zero))


async def sleep_to_work(hour, minute) -> int:
    # в этом блоке высчитываем сколько нам осталось спать до желаемого времени, в секундах
    now = datetime.datetime.now()
    target_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if target_time < now:
        # Если желаемое время уже прошло сегодня, то добавляем один день к целевому времени.
        target_time += datetime.timedelta(days=1)
    delta = target_time - now
    seconds_left = delta.total_seconds()
    return int(seconds_left)


async def prepare_send(state, user_name, user_id) -> None:
    data_state = await state.get_data()
    while True:
        try:
            logger_as.info(f'Подготовка к отправке файлов! {__name__}')
            gs = GS(family=user_name)
            data = gs.today_data_work()
            if data_state['auto_send_file'] == 'disable':
                break
            if 'выходной' not in data:
            # просыпаемся за 1 час до смены
                time = int(data[1][:-2]) - 2
                await asyncio.sleep(await sleep_to_work(hour=time,
                                                        minute=0))
                # выводим СЕГОДНЯ
                msg = await bot.send_message(chat_id=user_id,
                                             text=data[0])
                # тут юзаем функцию отправки! и запихиваем сюда какие спектакли надо подгрузить
                for_delete.update({user_id: [msg.message_id]})
                await auto_send(data[2], user_id)
                # после этого спим до нулей
                await asyncio.sleep(await time_to_zero())
                # удаляем все после нулей
                for id_s in for_delete[user_id]:
                    if len(for_delete[user_id]) == 0:
                        return None
                # добавить отлов ошибки????
                    await bot.delete_message(chat_id=user_id,
                                            message_id=id_s)
                    for_delete[user_id].remove(id_s)
            else:
                await asyncio.sleep(await time_to_zero())
        except Exception as ex:
            logger_as.error(ex, exc_info=True)


async def auto_send(data, user_id) -> None:
    # Флаг обозначен, чтобы лишний раз не заходить в цикл с поиском балета, если зашел в оперу
    flag = False
    for spec in data:
        for show in genre_show_f['Опера']:
            if show in spec and 'спектакл' in spec.lower():
                flag = True
                try:
                    logger_as.info(f'Отсылаем файлы! {__name__}')
                    files = FromYandex(genre='Опера',
                                       show=show,
                                       what='Паспорт спектакля').get_files()
                    if 'К сожалению, для' in files:
                        msg = await bot.send_message(chat_id=user_id,
                                                     text='К сожалению паспорт на этот спектакль отсутсвует,'
                                                          ' скоро это исправится!')
                        await asyncio.sleep(20)
                        await msg.delete()
                    else:
                        msg = await bot.send_message(chat_id=user_id,
                                                     text='Идет отправка файлов...')
                        for file in files:
                            document = URLInputFile(url=files[file],
                                                    filename=file)
                            doc_send = await bot.send_document(chat_id=user_id,
                                                               document=document)
                            for_delete.update({user_id: [doc_send.message_id]})
                        await msg.delete()
                except Exception as ex:
                    logger_as.error(ex, exc_info=True)
        if not flag:
            for show in genre_show_f['Балет']:
                if show in spec and 'спектакл' in spec.lower():
                    try:
                        logger_as.info(f'Отсылаем файлы! {__name__}')
                        files = FromYandex(genre='Балет',
                                           show=show,
                                           what='Паспорт спектакля').get_files()
                        if 'К сожалению, для' in files:
                            msg = await bot.send_message(chat_id=user_id,
                                                         text='К сожалению паспорт на этот спектакль отсутсвует,'
                                                              ' скоро это исправится!')
                            await asyncio.sleep(20)
                            await msg.delete()
                        else:
                            msg = await bot.send_message(chat_id=user_id,
                                                         text='Идет отправка файлов...')
                            for file in files:
                                document = URLInputFile(url=files[file],
                                                        filename=file)
                                doc_send = await bot.send_document(chat_id=user_id,
                                                                   document=document)
                                for_delete.update({user_id: [doc_send.message_id]})
                            await msg.delete()
                    except Exception as ex:
                        logger_as.error(ex, exc_info=True)
