from aiogram.filters import Text
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from config_data.data import TimeTable, Genre, ChoosePassport, Settings
from config_data.secret import logs_path
from keyboards.reply_markup.reply_builder import MainReplyKeyboard, MultiKeyboard
from keyboards.reply_inline.inline_builder import DiskInlineKeyboard
from disk_api.yandex_ import Passport
from aiogram import Router
from loguru import logger

"""loging"""
logger.add(logs_path+'/back_button.log', format='{time} {level} {message}', level='INFO', mode='w')

router_back = Router()


# # Тут отлавлием переход назад с обычной клавиатуры
# @router_back.message(Text('Назад'))
# async def back(message: Message, state: FSMContext) -> None:
#     user_data = await state.get_data()
#     keyboard = user_data['whitch_kb_was']
#     if keyboard == 'сhoose_jenre_kb':
#         keyboard = MultiKeyboard(Genre).build()
#         msg = await message.answer(text='Пожалуйста выберите жанр',
#                                    reply_markup=keyboard.as_markup())
#     elif keyboard == 'time_table_kb':
#         keyboard = MultiKeyboard(TimeTable).build()
#         msg = await message.answer(text='Пожалуйста выберите интересующий вас пункт',
#                                    reply_markup=keyboard.as_markup())
#         await state.update_data(whitch_kb_was='main_kb')
#     elif keyboard == 'calendar_kb':
#         keyboard = MainReplyKeyboard().build()
#         msg = await message.answer(text='Открываю главное меню!',
#                                    reply_markup=keyboard.as_markup())
#     elif keyboard == 'user_settings_kb':
#         keyboard = MultiKeyboard(Settings).build()
#         msg = await message.answer(text='Открываю главное меню!',
#                                    reply_markup=keyboard.as_markup())
#         await state.update_data(whitch_kb_was='main_kb')
#     elif keyboard == 'main_kb':
#         keyboard = MainReplyKeyboard().build()
#         msg = await message.answer(text='Открываю главное меню!',
#                                    reply_markup=keyboard.as_markup())
#     elif keyboard == 'choose_opera_kb':
#         genre = Passport('Опера')
#         keyboard = await DiskInlineKeyboard(genre).build()
#         msg = await message.answer(text='Пожалуйста выберите спектакль!',
#                                    reply_markup=keyboard.as_markup())
#     elif keyboard == 'choose_balet_kb':
#         genre = Passport('Балет')
#         keyboard = await DiskInlineKeyboard(genre).build()
#         msg = await message.answer(text='Пожалуйста выберите спектакль!!',
#                                    reply_markup=keyboard.as_markup())
#     elif keyboard == 'сhoose_what_need_kb':
#         keyboard = MultiKeyboard(ChoosePassport).build()
#         msg = await message.answer(text='Пожалуйста выберите вид выписки!',
#                                    reply_markup=keyboard.as_markup())
#     else:
#         msg = await message.answer(text='Проблема в choose_kb')
#     await message.delete()
#     await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
#                                                               message_id=msg.message_id,
#                                                               state=state)


class HandlerBack:
    """Обработчик апдейтов от BackRouter"""

    def __init__(self, message: Message, state: FSMContext):
        self.message = message
        self.state = state

    async def handler(self):
        keyboard_mapping = {
            'сhoose_jenre_kb': (MultiKeyboard(Genre), 'Пожалуйста выберите жанр'),
            'time_table_kb': (MultiKeyboard(TimeTable), 'Пожалуйста выберите интересующий вас пункт'),
            'calendar_kb': (MainReplyKeyboard(), 'Открываю главное меню!'),
            'user_settings_kb': (MultiKeyboard(Settings), 'Открываю главное меню!'),
            'main_kb': (MainReplyKeyboard(), 'Открываю главное меню!'),
            'choose_opera_kb': (await DiskInlineKeyboard(Passport('Опера')).build(), 'Пожалуйста выберите спектакль!'),
            'choose_balet_kb': (await DiskInlineKeyboard(Passport('Балет')).build(), 'Пожалуйста выберите спектакль!!'),
            'сhoose_what_need_kb': (MultiKeyboard(ChoosePassport), 'Пожалуйста выберите вид выписки!')
        }

        user_data = await self.state.get_data()
        keyboard, answer_text = keyboard_mapping.get(user_data['whitch_kb_was'], (None, 'Ошибка клавиатуры'))
        if keyboard is None:
            logger.error(f'Ошибка в клавиатуре, данные: keyboard:{keyboard}, answer:{answer_text}')
            await self.message.answer(text=answer_text)
        await self.state.update_data(whitch_kb_was='main_kb')
        await self.message.answer(text=answer_text, reply_markup=keyboard.as_markup())
        await self.message.delete()


class BackRouter(HandlerBack):
    """Роутер, который принимает апдейты"""

    @staticmethod
    @router_back.message(Text('Назад'))
    async def back(message: Message, state: FSMContext):
        super().__init__(message, state)
