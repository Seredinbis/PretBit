import support_function

from aiogram import Router
from aiogram.filters import Text
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.reply_markup.statements import choose_jenre_kb, choose_what_need_kb
from keyboards.reply_markup.main import main_kb
from keyboards.reply_inline.choose_show import choose_opera_kb, choose_balet_kb
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from disk_api.yandex_d import FromYandex


router_statement = Router()


# кнопка переводит в клавиатуру выбора жанра
@router_statement.message(Text('Выписки'))
async def get_statement(message: Message, state: FSMContext) -> None:
    await support_function.user_tracking.where_who(where=message.text,
                                                   state=state)
    if await support_function.login_test.log_test(message=message,
                                                  state=state):
        msg = await message.answer(text='Пожалуйста выберите жанр',
                                   reply_markup=choose_jenre_kb)
        await state.update_data(whitch_kb_was='main_kb')
        await message.delete()
        await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                                  message_id=msg.message_id,
                                                                  state=state)


# 2 кнопки выбора жанра Опера и Балет
@router_statement.message(Text(['Опера', 'Балет']))
async def choose_genre(message: Message, state: FSMContext) -> None:
    await support_function.user_tracking.where_who(where=message.text,
                                                   state=state)
    if await support_function.login_test.log_test(message=message,
                                                  state=state):
        if message.text == 'Опера':
            msg = await message.answer(text='Пожалуйста выберите интересующий вас спектакль!',
                                       reply_markup=choose_opera_kb)
            await state.update_data(genre='Опера')
        elif message.text == 'Балет':
            msg = await message.answer(text='Пожалуйста выберите интересующий вас спектакль!',
                                       reply_markup=choose_balet_kb)
            await state.update_data(genre='Балет')
        else:
            msg = await message.answer(text='Проблема в choose_genre')
        await state.update_data(genre=message.text)
        await state.update_data(whitch_kb_was='сhoose_jenre_kb')
        await message.delete()
        await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                                  message_id=msg.message_id,
                                                                  state=state)


# понимаем, какой вид выписки хотим и строим тут же клавиатуру, с файлами
@router_statement.message(Text(['Паспорт спектакля', 'Выписка водящего', 'Выписка спектакля']))
async def choose_what_plus_kb(message: Message, state: FSMContext) -> None:
    await support_function.user_tracking.where_who(where=message.text,
                                                   state=state)
    if await support_function.login_test.log_test(message=message,
                                                  state=state):
        await state.update_data(whitch_kb_was='сhoose_what_need_kb')
        await state.update_data(what=message.text)
        user_data = await state.get_data()
        files_dict = FromYandex(user_data['genre'], user_data['show'], user_data['what']).get_files()
        # начинаем строить клавиатуру если что-то вернулось
        if type(files_dict) == str:
            msg = await message.answer(text=files_dict,
                                       reply_markup=choose_what_need_kb)
            if user_data['genre'] == 'Опера':
                await state.update_data(whitch_kb_was='choose_opera_kb')
            elif user_data['genre'] == 'Балет':
                await state.update_data(whitch_kb_was='choose_balet_kb')
        else:
            # из-за того, что коллбэк ограничен 64 битами мы не можем запихнуть туда ссылку
            # создаем словарь с типа {ид ссылки: ссылка} и запихиваем его в стэйт
            # counter переводим в str - callback_data автоматом переводи в str
            url_id = {}
            counter = 0
            choose_file = InlineKeyboardBuilder()
            for file_name in files_dict:
                counter += 1
                file_url = files_dict[file_name]
                url_id.update({str(counter): [file_url, file_name]})
                await state.update_data(url_id=url_id)
                choose_file.row(InlineKeyboardButton(text=file_name,
                                                     callback_data=str(counter)))
            choose_file.row(InlineKeyboardButton(text='Назад',
                                                 callback_data='Назад к выбору вида выписки'))
            choose_file.row(InlineKeyboardButton(text='Вернуться в главное меню',
                                                 callback_data='Вернуться в главное меню'))
            msg = await message.answer(text='Пожалуйста, выберите необходимы вам файлы!',
                                       reply_markup=choose_file.as_markup())
        await message.delete()
        await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                                  message_id=msg.message_id,
                                                                  state=state)

@router_statement.message(Text('Вернуться в главное меню'))
async def choose_kb(message: Message, state: FSMContext) -> None:
    await support_function.user_tracking.where_who(where=message.text,
                                                   state=state)
    if await support_function.login_test.log_test(message=message,
                                                  state=state):
        msg = await message.answer(text='Открываю главное меню!',
                                   reply_markup=main_kb)
        await message.delete()
        await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                                  message_id=msg.message_id,
                                                                  state=state)
