from aiogram import Router
from aiogram.filters import Text
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.reply_markup.reply_builder import CalendarReplyKeyboard
from sql_data.sql import session, Employee
from sheets_api.gs_pandas import LightPerson
from config_data.fltrs import day_number
from loguru import logger


router_calendar = Router()


class HandlerCalendar:
    """Обработчик апдейтов календаря"""

    @staticmethod
    @router_calendar.message(Text('Календарь'))
    async def handler_days(message: Message, state: FSMContext) -> None:
        """Возвращает клавиатуру с днями месяца"""

        logger.info(f'Пользователь с tg_id {message.from_user.id} вызвал клавиатуру календаря')
        keyboard = CalendarReplyKeyboard().build()
        await message.answer(text='Выберите пожалуйста желаемую дату текущего месяца',
                             reply_markup=keyboard.as_markup())
        await state.update_data(whitch_kb_was='main_kb')
        await message.delete()

    @staticmethod
    @router_calendar.message(Text(day_number))
    async def handler_day(message: Message, state: FSMContext) -> None:
        """Возвращает информацию по конкретному дню из графика для конкретного пользователя"""

        with session as ses:
            user_sn = ses.query(Employee.last_name).filter(Employee.id == message.from_user.id).scalar()

        logger.info(f'{user_sn} отправил запрос на получение {message.text} дня')
        await message.delete()
        await state.update_data(whitch_kb_was='calendar_kb')
        msg = await message.answer(text='Идет загрузка...')
        keyboard = CalendarReplyKeyboard().build()
        await message.answer(text=LightPerson(last_name=user_sn, day=message.text).get_message(),
                             reply_markup=keyboard.as_markup())
        await msg.delete()
