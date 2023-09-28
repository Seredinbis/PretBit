import support_function

from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from bot import bot
from aiogram.types.input_file import URLInputFile
from keyboards.reply_markup.statements import choose_jenre_kb, choose_what_need_kb
from keyboards.reply_markup.main import main_kb
from keyboards.reply_inline.choose_show import choose_manual_kb
from keyboards.reply_markup.user_setting import user_settings_kb
from .fltrs.all_filters import genre_show_f
from .fltrs.all_filters import how_mutch_delete_fltr, how_mutch_delete_file_fltr, csn
from disk_api.yandex_d import Manual, Chain
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from .fltrs.all_filters import work_position
from keyboards.reply_inline.choose_position import choose_work_pos
from sql_data.sql import session, Employee, Position

router_callbacks = Router()


@router_callbacks.callback_query(lambda call: call.data in work_position or call.data in csn)
async def set_user_second_name(callback: CallbackQuery, state: FSMContext) -> None:
    user_data = await state.get_data()
    if callback.data in work_position:
        a_to_table = Position(name=callback.data,
                              employees_id=callback.from_user.id)
        with session as s:
            s.add(a_to_table)
            s.commit()
        await state.update_data(login=True)
        msg = await bot.send_message(chat_id=callback.from_user.id,
                                     text='Открываю главное меню!',
                                     reply_markup=main_kb)
        await support_function.delete_pre_message.del_pre_message(chat_id=callback.from_user.id,
                                                                  message_id=msg.message_id,
                                                                  state=state)
        await support_function.prepare_send(state=state,
                                            user_id=callback.from_user.id,
                                            user_name=user_data['user_second_name'])
    elif 'user_second_name' not in user_data:
        if callback.data in ('Василевский', 'Круссер'):
            await state.update_data(user_second_name=None)
            await callback.answer(text=f'Вы выбрали {callback.data}\nК сожалению вас нет в графике,'
                                       f' часть функций будет недоступна',
                                  show_alert=True)
            a_to_table = Employee(id=callback.from_user.id,
                                  last_name=callback.data)
            with session as s:
                s.add(a_to_table)
                s.commit()
            msg = await bot.send_message(chat_id=callback.from_user.id,
                                         text='Пожалуйста выберите свою должность!',
                                         reply_markup=choose_work_pos.as_markup())
            await support_function.delete_pre_message.del_pre_message(chat_id=callback.from_user.id,
                                                                      message_id=msg.message_id,
                                                                      state=state)
        else:
            await callback.answer(text=f'Вы выбрали {callback.data}\nВыбор соответсвующей фамилии напрямую зависит на'
                                       f' корректную работу бота!',
                                  show_alert=True)
            a_to_table = Employee(id=callback.from_user.id,
                                  last_name=callback.data)
            with session as s:
                s.add(a_to_table)
                s.commit()
            await state.update_data(user_second_name=callback.data)
            msg = await bot.send_message(chat_id=callback.from_user.id,
                                         text='Пожалуйста выберите свою должность!',
                                         reply_markup=choose_work_pos.as_markup())
            await support_function.delete_pre_message.del_pre_message(chat_id=callback.from_user.id,
                                                                      message_id=msg.message_id,
                                                                      state=state)


@router_callbacks.callback_query(lambda call: call.data in how_mutch_delete_fltr)
async def how_mutch_del_pre(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(i_can_del_mess=True)
    await state.update_data(how_del=callback.data[0])
    msg = await bot.send_message(text=f'Cообщения присланные вам будут удаляться после {callback.data[0]} присланных'
                                      f' сообщений',
                                 chat_id=callback.from_user.id,
                                 reply_markup=user_settings_kb)
    await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                              message_id=msg.message_id,
                                                              state=state)


@router_callbacks.callback_query(lambda call: call.data in how_mutch_delete_file_fltr)
async def how_mutch_del_files(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(i_can_del_file=True)
    await state.update_data(how_del_files=callback.data[0])
    msg = await bot.send_message(text=f'Файлы присланные вам будут удаляться через {callback.data[0]} час(а)(ов)',
                                 chat_id=callback.from_user.id,
                                 reply_markup=user_settings_kb)
    await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                              message_id=msg.message_id,
                                                              state=state)


@router_callbacks.callback_query(lambda call: call.data.startswith('ЛЕБЕДКИ '))
async def get_lebed(callback: CallbackQuery, state: FSMContext) -> None:
    files_list = Chain(show=callback.data[8::]).get_files()[0]
    document = URLInputFile(url=files_list[1],
                            filename=files_list[0])
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
        files_dict = Manual(device).get_file()
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
    msg = await bot.send_message(text='Открываю главное меню!',
                                 chat_id=callback.from_user.id,
                                 reply_markup=main_kb)
    await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                              message_id=msg.message_id,
                                                              state=state)
    await state.update_data(whitch_kb_was='main_kb')


@router_callbacks.callback_query(lambda call: call.data.startswith('Назад'))
async def go_back(callback: CallbackQuery, state: FSMContext) -> None:
    user_data = await state.get_data()
    if callback.data == 'Назад к выбору жанра':
        msg = await bot.send_message(text='Пожалуйста выберите жанр',
                                     chat_id=callback.from_user.id,
                                     reply_markup=choose_jenre_kb)
        await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                                  message_id=msg.message_id,
                                                                  state=state)
        await state.update_data(whitch_kb_was='main_kb')
    elif callback.data == 'Назад к выбору мануала':
        msg = await bot.send_message(text='Пожалуйста выберите мануал',
                                     chat_id=callback.from_user.id,
                                     reply_markup=choose_manual_kb)
        await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                                  message_id=msg.message_id,
                                                                  state=state)
    elif callback.data == 'Назад к выбору настроек':
        msg = await bot.send_message(text='Пожалуйста выберите необходимую настройку',
                                     chat_id=callback.from_user.id,
                                     reply_markup=user_settings_kb)
        await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                                  message_id=msg.message_id,
                                                                  state=state)
    elif callback.data == 'Назад к выбору вида выписки':
        msg = await bot.send_message(text='Пожалуйста выберите вид выписки!',
                                     chat_id=callback.from_user.id,
                                     reply_markup=choose_what_need_kb)
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
        msg = await bot.send_message(text='Пожалуйста выберите вид паспорта/выписки',
                                     chat_id=callback.from_user.id,
                                     reply_markup=choose_what_need_kb)
        if genre == 'Опера':
            await state.update_data(whitch_kb_was='choose_opera_kb')
        else:
            await state.update_data(whitch_kb_was='choose_balet_kb')
        await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                                  message_id=msg.message_id,
                                                                  state=state)
