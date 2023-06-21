import support_function

from aiogram import Router
from aiogram.filters import Text
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.reply_markup.time_table import time_table_kb
from keyboards.reply_markup.month_choose import month_choose_kb
from .fltrs.all_filters import month
from sheets_api.gs import GS
router_time_table = Router()


@router_time_table.message(Text('График'))
async def time_table_menu(message: Message, state: FSMContext) -> None:
    await support_function.user_tracking.where_who(where=message.text,
                                                   state=state)
    msg = await message.answer(text='Пожалуйста выберите интересующий вас пункт!',
                               reply_markup=time_table_kb)
    await state.update_data(whitch_kb_was='main_kb')
    await message.delete()
    await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                              message_id=msg.message_id,
                                                              state=state)


@router_time_table.message(Text('Общий график'))
async def get_all_time_table(message: Message, state: FSMContext) -> None:
    url = 'https://docs.google.com/spreadsheets/d/1iw2mz3md74UeCIMy3eXnfBH-E2-rhwBkWosxwVZVJxM/edit#gid=885283339'
    await support_function.user_tracking.where_who(where=message.text,
                                                   state=state)
    msg = await message.answer(text=url,
                               reply_markup=time_table_kb)
    await state.update_data(whitch_kb_was='main_kb')
    await message.delete()
    await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                              message_id=msg.message_id,
                                                              state=state)


@router_time_table.message(Text('Персональный график'))
async def get_personal_time_table(message: Message, state: FSMContext) -> None:
    await support_function.user_tracking.where_who(where=message.text,
                                                   state=state)
    msg = await message.answer(text='Данная функция находится в разработке',
                               reply_markup=time_table_kb)
    await state.update_data(whitch_kb_was='main_kb')
    await message.delete()
    await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                              message_id=msg.message_id,
                                                              state=state)


@router_time_table.message(Text('Количество отработанных часов'))
async def time_table_menu(message: Message, state: FSMContext) -> None:
    await support_function.user_tracking.where_who(where=message.text,
                                                   state=state)
    if await support_function.login_test.log_test(message=message,
                                                  state=state):
        msg = await message.answer(text='Выберите  интересующий вас пункт!',
                                   reply_markup=month_choose_kb.as_markup())
        await state.update_data(whitch_kb_was='time_table_kb')
        await message.delete()
        await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                                  message_id=msg.message_id,
                                                                  state=state)


@router_time_table.message(Text(month))
async def time_table_menu(message: Message, state: FSMContext) -> None:
    month_choose = ['',
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
    await support_function.user_tracking.where_who(where=message.text,
                                                   state=state)
    if await support_function.login_test.log_test(message=message,
                                                  state=state):
        user_data = await state.get_data()
        user_sn = user_data['user_second_name']
        if user_sn == 'Василевский' or user_sn == 'Крусер':
            user_sn = 'Быкова'
        await message.delete()
        if message.text == 'За все отработанное время':
            msg = await message.answer(text='Идет загрузка...')
            await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                                      message_id=msg.message_id,
                                                                      state=state)
            msg1 = await message.answer(text=GS(family=user_sn).work_hour_all(),
                                        reply_markup=month_choose_kb.as_markup(),
                                        parse_mode='HTML')
            await state.update_data(whitch_kb_was='time_table_kb')
            await support_function.delete_pre_message.del_pre_message(chat_id=msg1.chat.id,
                                                                      message_id=msg1.message_id,
                                                                      state=state)
        else:
            msg = await message.answer(text='Идет загрузка...')
            await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                                      message_id=msg.message_id,
                                                                      state=state)
            msg1 = await message.answer(text=GS(family=user_sn,
                                                month=month_choose.index(message.text)).work_hour_mounth(),
                                        reply_markup=month_choose_kb.as_markup(),
                                        parse_mode='HTML')
            await state.update_data(whitch_kb_was='time_table_kb')
            await support_function.delete_pre_message.del_pre_message(chat_id=msg1.chat.id,
                                                                      message_id=msg1.message_id,
                                                                      state=state)
