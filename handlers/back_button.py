import support_function

from aiogram.filters import Text
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.reply_markup.time_table import time_table_kb
from keyboards.reply_markup.statements import choose_jenre_kb, choose_what_need_kb
from keyboards.reply_markup.main import main_kb
from keyboards.reply_inline.choose_show import choose_opera_kb, choose_balet_kb
from keyboards.reply_markup.user_setting import user_settings_kb
from aiogram import Router

router_back = Router()


# Тут отлавлием переход назад с обычной клавиатуры
@router_back.message(Text('Назад'))
async def back(message: Message, state: FSMContext) -> None:
    await support_function.user_tracking.where_who(where=message.text,
                                                   state=state)
    user_data = await state.get_data()
    if await support_function.login_test.log_test(message=message,
                                                  state=state):
        keyboard = user_data['whitch_kb_was']
        if keyboard == 'сhoose_jenre_kb':
            msg = await message.answer(text='Пожалуйста выберите жанр',
                                       reply_markup=choose_jenre_kb)
        elif keyboard == 'time_table_kb':
            msg = await message.answer(text='Пожалуйста выберите интересующий вас пункт',
                                       reply_markup=time_table_kb)
            await state.update_data(whitch_kb_was='main_kb')
        elif keyboard == 'calendar_kb':
            msg = await message.answer(text='Открываю главное меню!',
                                       reply_markup=main_kb)
        elif keyboard == 'user_settings_kb':
            msg = await message.answer(text='Открываю главное меню!',
                                       reply_markup=user_settings_kb)
            await state.update_data(whitch_kb_was='main_kb')
        elif keyboard == 'main_kb':
            msg = await message.answer(text='Открываю главное меню!',
                                       reply_markup=main_kb)
        elif keyboard == 'choose_opera_kb':
            msg = await message.answer(text='Пожалуйста выберите спектакль!',
                                       reply_markup=choose_opera_kb)
        elif keyboard == 'choose_balet_kb':
            msg = await message.answer(text='Пожалуйста выберите спектакль!!',
                                       reply_markup=choose_balet_kb)
        elif keyboard == 'сhoose_what_need_kb':
            msg = await message.answer(text='Пожалуйста выберите вид выписки!',
                                       reply_markup=choose_what_need_kb)
        else:
            msg = await message.answer(text='Проблема в choose_kb')
        await message.delete()
        await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                                  message_id=msg.message_id,
                                                                  state=state)
