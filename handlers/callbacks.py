import support_function

from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from bot import bot
from aiogram.types.input_file import URLInputFile
from keyboards.reply_markup.statements import choose_jenre_kb, choose_what_need_kb
from keyboards.reply_markup.main import main_kb
from .fltrs.all_filters import genre_show_f
from other_data import working_positions
from .fltrs.all_filters import csn

router_callbacks = Router()


# фильтр на содержание даты в тюпле фамилий
@router_callbacks.callback_query(lambda call: call.data in csn)
async def set_user_second_name(callback: CallbackQuery, state: FSMContext) -> None:
    user_data = await state.get_data()
    await state.update_data(login=True)
    if 'user_seecond_name' in user_data:
        await callback.answer(text=f'Вы уже выбрали {user_data["user_second_name"]}',
                              show_alert=True)
    else:
        if callback.data in ('Василевский', 'Круссер'):
            await state.update_data(user_second_name='Быкова')
            await callback.answer(text=f'Вы выбралию {callback.data}\nК сожалению вас нет в графике, вы будете'
                                       f' пользоваться ботом под фамилией Быкова',
                                  show_alert=True)
        else:
            await callback.answer(text=f'Вы выбралию {callback.data}\nВыбор соответсвующей фамилии напрямую зависит на'
                                       f' корректную работу бота!',
                                  show_alert=True)
            await state.update_data(user_second_name=callback.data)
        await state.update_data(user_working_position=working_positions[callback.data])
        msg = await bot.send_message(chat_id=callback.from_user.id,
                                     text='Открываю главное меню!',
                                     reply_markup=main_kb)
        await support_function.delete_pre_message.del_pre_message(chat_id=callback.from_user.id,
                                                                  message_id=msg.message_id,
                                                                  state=state)

@router_callbacks.callback_query()
async def callbacks(callback: CallbackQuery, state: FSMContext) -> None:
    user_data = await state.get_data()
    genre = user_data['genre']
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
    elif callback.data == 'Назад к выбору жанра':
        msg = await bot.send_message(text='Пожалуйста выберите жанр',
                                     chat_id=callback.from_user.id,
                                     reply_markup=choose_jenre_kb)
        await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                                  message_id=msg.message_id,
                                                                  state=state)
        await state.update_data(whitch_kb_was='main_kb')
    elif callback.data == 'Вернуться в главное меню':
        msg = await bot.send_message(text='Открываю главное меню!',
                                     chat_id=callback.from_user.id,
                                     reply_markup=main_kb)
        await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                                  message_id=msg.message_id,
                                                                  state=state)
        await state.update_data(whitch_kb_was='main_kb')
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
    elif callback.data in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10'):
        url = user_data['url_id'][callback.data][0]
        name = user_data['url_id'][callback.data][1]
        document = URLInputFile(url=url,
                                filename=name)
        send = await bot.send_document(chat_id=callback.from_user.id,
                                       document=document)
        # пока удаления нет, но есть айди всех файлов
        await support_function.delete_file_after.del_files(chat_id=send.chat.id,
                                                           file_id=send.message_id)
