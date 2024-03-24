import support_function

from aiogram import Router
from aiogram.filters import Text
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.reply_markup.reply_builder import MultiKeyboard
from config_data.data import TimeTable
from config_data.secret import time_table_url
from keyboards.reply_markup.reply_builder import MonthKeyboard
from config_data.fltrs.all_filters import month
from sheets_api.gs_pandas import LightPerson
from sql_data.sql import session, Employee
from loguru import logger


router_time_table = Router()


@router_time_table.message(Text('График'))
async def time_table_menu(message: Message, state: FSMContext) -> None:
    """Отправляет клавиатуру с выбором месяца"""

    logger.info(f'Пользователь с tg_id {message.from_user.id} запросил выборку месяца')
    keyboard = MultiKeyboard(TimeTable).build()
    msg = await message.answer(text='Пожалуйста выберите интересующий вас пункт!',
                               reply_markup=keyboard.as_markup())
    await state.update_data(whitch_kb_was='main_kb')
    await message.delete()
    await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                              message_id=msg.message_id,
                                                              state=state)


@router_time_table.message(Text('Общий график'))
async def get_all_time_table(message: Message, state: FSMContext) -> None:
    """Отправляет ссылку на график"""

    logger.info(f'Пользователь с tg_id {message.from_user.id} запросил ссылку на график')
    keyboard = MultiKeyboard(TimeTable).build()
    msg = await message.answer(text=time_table_url,
                               reply_markup=keyboard.as_markup())
    await state.update_data(whitch_kb_was='main_kb')
    await message.delete()
    await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                              message_id=msg.message_id,
                                                              state=state)


@router_time_table.message(Text('Персональный график'))
async def get_personal_time_table(message: Message, state: FSMContext) -> None:
    """Отправляет персональный график"""

    logger.info(f'Пользователь с tg_id {message.from_user.id} запросил персональный график')
    keyboard = MultiKeyboard(TimeTable).build()
    msg = await message.answer(text='Данная функция находится в разработке',
                               reply_markup=keyboard.as_markup())
    await state.update_data(whitch_kb_was='main_kb')
    await message.delete()
    await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                              message_id=msg.message_id,
                                                              state=state)


@router_time_table.message(Text('Количество отработанных часов'))
async def time_table_menu(message: Message, state: FSMContext) -> None:
    """Отправляет клавиатуру выбора месяца, в котором хотим узнать отработанное время"""

    logger.info(f'Пользователь с tg_id {message.from_user.id} запросил кол-во отработанных часов, за все время')
    if await support_function.login_test.log_test(message=message):
        keyboard = MonthKeyboard().build()
        msg = await message.answer(text='Выберите  интересующий вас пункт!',
                                   reply_markup=keyboard.as_markup())
        await state.update_data(whitch_kb_was='time_table_kb')
        await message.delete()
        await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                                  message_id=msg.message_id,
                                                                  state=state)


@router_time_table.message(Text(month))
async def time_table_menu(message: Message, state: FSMContext) -> None:
    """Отправляет кол-во отработанных часов за конкретный месяц, либо за все время"""

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
    if await support_function.login_test.log_test(message=message):
        with session as ses:
            user_sn = ses.query(Employee.last_name).filter(Employee.id == message.from_user.id).scalar()
        if user_sn == 'Василевский' or user_sn == 'Крусер':
            user_sn = 'Быкова'
        await message.delete()
        if message.text == 'За все отработанное время':
            logger.info(f'Пользователь с tg_id {message.from_user.id} запросил кол-во отработанных часов')
            msg = await message.answer(text='Идет загрузка...')
            await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                                      message_id=msg.message_id,
                                                                      state=state)
            all_time = LightPerson(last_name=user_sn).get_all_time()
            if all_time[0] is None:
                add = ''
            add = all_time[0]
            keyboard = MonthKeyboard().build()
            msg1 = await message.answer(text=f'Количество отработанного времени за утченные месяцы составляет'
                                             f' <b>{all_time[1]}</b>!\n' + add,
                                        reply_markup=keyboard.as_markup(),
                                        parse_mode='HTML')
            await state.update_data(whitch_kb_was='time_table_kb')
            await support_function.delete_pre_message.del_pre_message(chat_id=msg1.chat.id,
                                                                      message_id=msg1.message_id,
                                                                      state=state)
        else:
            logger.info(f'Пользователь с tg_id {message.from_user.id} запросил кол-во отработанных часов,'
                        f' за {message.text}')
            msg = await message.answer(text='Идет загрузка...')
            await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                                      message_id=msg.message_id,
                                                                      state=state)
            keyboard = MonthKeyboard().build()
            msg1 = await message.answer(text=LightPerson(last_name=user_sn,
                                                         month=month_choose.index(message.text)).get_month_time(),
                                        reply_markup=keyboard.as_markup(),
                                        parse_mode='HTML')
            await state.update_data(whitch_kb_was='time_table_kb')
            await support_function.delete_pre_message.del_pre_message(chat_id=msg1.chat.id,
                                                                      message_id=msg1.message_id,
                                                                      state=state)
