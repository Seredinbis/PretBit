from aiogram.filters import Text
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from config_data.data import TimeTable, Genre, ChoosePassport, Settings
from keyboards.reply_markup.reply_builder import MainReplyKeyboard, MultiKeyboard
from keyboards.reply_inline.inline_builder import DiskInlineKeyboard
from disk_api.yandex_ import Passport
from aiogram import Router
from loguru import logger


router_back = Router()


class HandlerBack:
    """Обработчик апдейтов кнопок Назад"""

    @staticmethod
    @router_back.message(Text('Назад'))
    async def handler(message: Message, state: FSMContext) -> None:
        keyboard_mapping = {
            'сhoose_jenre_kb': (MultiKeyboard(Genre).build(), 'Пожалуйста выберите жанр'),
            'time_table_kb': (MultiKeyboard(TimeTable).build(), 'Пожалуйста выберите интересующий вас пункт'),
            'calendar_kb': (MainReplyKeyboard().build(), 'Открываю главное меню!'),
            'user_settings_kb': (MultiKeyboard(Settings).build(), 'Открываю главное меню!'),
            'main_kb': (MainReplyKeyboard().build(), 'Открываю главное меню!'),
            'choose_opera_kb': (await DiskInlineKeyboard(Passport('Опера')).build(), 'Пожалуйста выберите спектакль!'),
            'choose_balet_kb': (await DiskInlineKeyboard(Passport('Балет')).build(), 'Пожалуйста выберите спектакль!!'),
            'сhoose_what_need_kb': (MultiKeyboard(ChoosePassport).build(), 'Пожалуйста выберите вид выписки!')
        }

        user_data = await state.get_data()
        keyboard, answer_text = keyboard_mapping.get(user_data['whitch_kb_was'], (None, 'Ошибка клавиатуры'))
        if keyboard is None:
            logger.error(f'Ошибка в клавиатуре, данные: keyboard:{keyboard}, answer:{answer_text}')
            await message.answer(text=answer_text)
        await state.update_data(whitch_kb_was='main_kb')
        await message.answer(text=answer_text, reply_markup=keyboard.as_markup())
        await message.delete()
