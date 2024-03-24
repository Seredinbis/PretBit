import support_function

from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from bot import bot
from aiogram.types.input_file import URLInputFile
from keyboards.reply_markup.reply_builder import MainReplyKeyboard, MultiKeyboard
from config_data.data import Genre, Settings, ChoosePassport
from keyboards.reply_inline.inline_builder import DiskInlineKeyboard
from disk_api.yandex_ import Manual, Chain
from config_data.fltrs.all_filters import genre_show_f
from config_data.fltrs.all_filters import how_mutch_delete_fltr, how_mutch_delete_file_fltr
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from config_data.fltrs.all_filters import work_position
from keyboards.reply_inline.inline_builder import PositionsInlineKeyboard
from sheets_api.gs_pandas import GetInfo
from sql_data.sql import session, Employee, Position
from loguru import logger

router_callbacks = Router()


@router_callbacks.callback_query(lambda call: call.data in work_position or call.data in GetInfo().get_employees().keys())
async def set_user_second_name(callback: CallbackQuery, state: FSMContext) -> None:
    """callback на выбор фамилии из инлайн клавиатуры"""

    logger.info(f'Пользователь выбрал фамилию {callback.data}')
    if callback.data in work_position:
        with session as ses:
            user_ln = ses.query(Employee.last_name).filter(Employee.id == callback.from_user.id)
        a_to_table = Position(name=callback.data,
                              employees_id=callback.from_user.id)
        with session as s:
            s.add(a_to_table)
            s.commit()
        await state.update_data(login=True)
        keyboard = MainReplyKeyboard().build()
        msg = await bot.send_message(chat_id=callback.from_user.id,
                                     text='Открываю главное меню!',
                                     reply_markup=keyboard.as_markup())
        await support_function.delete_pre_message.del_pre_message(chat_id=callback.from_user.id,
                                                                  message_id=msg.message_id,
                                                                  state=state)
    elif support_function.login_test.log_test(callback):
        if callback.data in ('Василевский', 'Круссер'):
            await callback.answer(text=f'Вы выбрали {callback.data}\nК сожалению вас нет в графике,'
                                       f' часть функций будет недоступна',
                                  show_alert=True)
        else:
            await callback.answer(text=f'Вы выбрали {callback.data}\nВыбор соответсвующей фамилии напрямую зависит на'
                                       f' корректную работу бота!',
                                  show_alert=True)
        a_to_table = Employee(id=callback.from_user.id,
                              last_name=callback.data)
        with session as s:
            s.add(a_to_table)
            s.commit()
        keyboard = PositionsInlineKeyboard().build()
        msg = await bot.send_message(chat_id=callback.from_user.id,
                                     text='Пожалуйста выберите свою должность!',
                                     reply_markup=keyboard.as_markup())
        await support_function.delete_pre_message.del_pre_message(chat_id=callback.from_user.id,
                                                                  message_id=msg.message_id,
                                                                  state=state)


@router_callbacks.callback_query(lambda call: call.data in how_mutch_delete_fltr)
async def how_mutch_del_pre(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(i_can_del_mess=True)
    await state.update_data(how_del=callback.data[0])
    keyboard = MultiKeyboard(Settings).build()
    msg = await bot.send_message(text=f'Cообщения присланные вам будут удаляться после {callback.data[0]} присланных'
                                      f' сообщений',
                                 chat_id=callback.from_user.id,
                                 reply_markup=keyboard.as_markup())
    await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                              message_id=msg.message_id,
                                                              state=state)


@router_callbacks.callback_query(lambda call: call.data in how_mutch_delete_file_fltr)
async def how_mutch_del_files(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(i_can_del_file=True)
    await state.update_data(how_del_files=callback.data[0])
    keyboard = MultiKeyboard(Settings).build()
    msg = await bot.send_message(text=f'Файлы присланные вам будут удаляться через {callback.data[0]} час(а)(ов)',
                                 chat_id=callback.from_user.id,
                                 reply_markup=keyboard.as_markup())
    await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                              message_id=msg.message_id,
                                                              state=state)


@router_callbacks.callback_query(lambda call: call.data.startswith('ЛЕБЕДКИ '))
async def get_lebed(callback: CallbackQuery, state: FSMContext) -> None:
    show = callback.data[8::]
    files = await Chain(show).get_files()
    (name, url), = files.items()
    document = URLInputFile(url=url,
                            filename=name)
    send = await bot.send_document(chat_id=callback.from_user.id,
                                   document=document)
    await support_function.delete_file_after.del_files(chat_id=send.chat.id,
                                                       file_id=send.message_id,
                                                       state=state)


@router_callbacks.callback_query(lambda call: call.data.startswith('МАНУАЛ '))
async def get_manuall(callback: CallbackQuery, state: FSMContext) -> None:
    if callback.data.startswith('МАНУАЛ '):
        device = callback.data[7::]
        dict_for_call_send = {}
        files_dict = await Manual(device).get_files()
        # cоставляем инлайн клавиатуру из полученного словаря
        choose_manual_file_kb = InlineKeyboardBuilder()
        counter = 0
        for files in files_dict:
            dict_for_call_send.update({counter: [files, files_dict[files]]})
            choose_manual_file_kb.row(InlineKeyboardButton(text=files,
                                                           callback_data=f'* {counter}'))
            counter += 1
        # вводим это в стейт, чтобы не создавать отдельную глобальную переменную
        # локальная переменная тут тоже не подойдет, так как хэндлер при каждом коллбэке будет ловиться заново
        await state.update_data(manual=dict_for_call_send)
        choose_manual_file_kb.row(InlineKeyboardButton(text='Назад',
                                                       callback_data='Назад к выбору манула'))
        choose_manual_file_kb.row(InlineKeyboardButton(text='В главное меню',
                                                       callback_data='Вернуться в главное меню'))
        msg = await bot.send_message(chat_id=callback.from_user.id,
                                     text='Пожалуйста, выберите необходимый файл',
                                     reply_markup=choose_manual_file_kb.as_markup())
        await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                                  message_id=msg.message_id,
                                                                  state=state)


@router_callbacks.callback_query(lambda call: call.data.startswith('* '))
async def if_whitch_star(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    dict_for_call_send = data['manual']
    document = URLInputFile(url=dict_for_call_send[callback.data[2::]][1],
                            filename=dict_for_call_send[callback.data[2::]][0])
    send = await bot.send_document(chat_id=callback.from_user.id,
                                   document=document)
    await support_function.delete_file_after.del_files(chat_id=send.chat.id,
                                                       file_id=send.message_id,
                                                       state=state)


@router_callbacks.callback_query(lambda call: call.data == 'Вернуться в главное меню')
async def go_to_main(callback: CallbackQuery, state: FSMContext) -> None:
    keyboard = MainReplyKeyboard().build()
    msg = await bot.send_message(text='Открываю главное меню!',
                                 chat_id=callback.from_user.id,
                                 reply_markup=keyboard.as_markup())
    await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                              message_id=msg.message_id,
                                                              state=state)
    await state.update_data(whitch_kb_was='main_kb')


@router_callbacks.callback_query(lambda call: call.data.startswith('Назад'))
async def go_back(callback: CallbackQuery, state: FSMContext) -> None:
    user_data = await state.get_data()
    if callback.data == 'Назад к выбору жанра':
        keyboard = MultiKeyboard(Genre).build()
        msg = await bot.send_message(text='Пожалуйста выберите жанр',
                                     chat_id=callback.from_user.id,
                                     reply_markup=keyboard.as_markup())
        await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                                  message_id=msg.message_id,
                                                                  state=state)
        await state.update_data(whitch_kb_was='main_kb')
    elif callback.data == 'Назад к выбору мануала':
        data = Manual()
        keyboard = await DiskInlineKeyboard(data).build()
        msg = await bot.send_message(text='Пожалуйста выберите мануал',
                                     chat_id=callback.from_user.id,
                                     reply_markup=keyboard.as_markup())
        await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                                  message_id=msg.message_id,
                                                                  state=state)
    elif callback.data == 'Назад к выбору настроек':
        keyboard = MultiKeyboard(Settings).build()
        msg = await bot.send_message(text='Пожалуйста выберите необходимую настройку',
                                     chat_id=callback.from_user.id,
                                     reply_markup=keyboard.as_markup())
        await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                                  message_id=msg.message_id,
                                                                  state=state)
    elif callback.data == 'Назад к выбору вида выписки':
        keyboard = MultiKeyboard(ChoosePassport).build()
        msg = await bot.send_message(text='Пожалуйста выберите вид выписки!',
                                     chat_id=callback.from_user.id,
                                     reply_markup=keyboard.as_markup())
        await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                                  message_id=msg.message_id,
                                                                  state=state)
        if user_data['genre'] == 'Опера':
            await state.update_data(whitch_kb_was='choose_opera_kb')
        elif user_data['genre'] == 'Балет':
            await state.update_data(whitch_kb_was='choose_balet_kb')


# до 10 - потомучто вряд ли будет больше файлов в одной папке
@router_callbacks.callback_query(lambda call: call.data in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10'))
async def go_to_main(callback: CallbackQuery, state: FSMContext) -> None:
    user_data = await state.get_data()
    url = user_data['url_id'][callback.data][0]
    name = user_data['url_id'][callback.data][1]
    document = URLInputFile(url=url,
                            filename=name)
    send = await bot.send_document(chat_id=callback.from_user.id,
                                   document=document)
    # пока удаления нет, но есть айди всех файлов
    await support_function.delete_file_after.del_files(chat_id=send.chat.id,
                                                       file_id=send.message_id,
                                                       state=state)


@router_callbacks.callback_query()
async def callbacks(callback: CallbackQuery, state: FSMContext) -> None:
    user_data = await state.get_data()
    genre = user_data['genre']
    # в dict_for_call_send храниться список с именем файла и урл по номеру ключа
    if callback.data in genre_show_f[genre]:
        await state.update_data(show=callback.data)
        keyboard = MultiKeyboard(ChoosePassport).build()
        msg = await bot.send_message(text='Пожалуйста выберите вид паспорта/выписки',
                                     chat_id=callback.from_user.id,
                                     reply_markup=keyboard.as_markup())
        if genre == 'Опера':
            await state.update_data(whitch_kb_was='choose_opera_kb')
        else:
            await state.update_data(whitch_kb_was='choose_balet_kb')
        await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                                  message_id=msg.message_id,
                                                                  state=state)
