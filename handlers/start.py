import asyncio
import support_function

from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import Router
from aiogram.types import CallbackQuery
from keyboards.reply_inline.choose_second_name import choose_sn_kb
from keyboards.reply_inline.choose_position import choose_work_pos
from keyboards.reply_markup.main import main_kb
from sql_data.sql import session, Employee, Position
from bot import bot
from fltrs.all_filters import work_position

router_start = Router()


@router_start.message(Command(commands=["start"]))
async def start(message: Message, state: FSMContext) -> None:
    await support_function.user_tracking.where_who(where=message.text,
                                                   state=state)
    user_data: dict = await state.get_data()
    if len(user_data) == 0 or 'user_second_name' not in user_data or user_data['user_second_name'] == '':
        await state.update_data(user_id=str(message.from_user.id))
        msg = await message.answer(text='Пожалуйста, выберите СВОЮ фамилию из списка!',
                                   reply_markup=choose_sn_kb.as_markup())
        # Проверяем, обновлялся ли этот стейт через настройки, если да, то не обновляем сейчас
        # обновим user_data чтобы были корректные данные после выбора фамилиим
        user_data: dict = await state.get_data()
        # бесконечный цикл, ждет, пока юсер не нажмет фамилию на клаве, cпим 3 секунды, чтобы меньше гонять цикл и
        # чтобы коллбэк подгрузился
        while 'login' not in user_data:
            user_data = await state.get_data()
            await asyncio.sleep(1)
        await msg.delete()
        await message.delete()
    else:
        await message.delete()
        # Проверяем, обновлялся ли этот стейт через настройки, если да, то не обновляем сейчас
        # Тут на всякий случай, можно будет удалить
        msg = await message.answer(text='Вы уже залогинены, приятного общения с ботом!\n/about - тут можно узнать всю'
                                        ' информацию о боте.\n',
                                   reply_markup=main_kb)
        await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                                  message_id=msg.message_id,
                                                                  state=state)


@router_start.message(Command(commands=["about"]))
async def about_bot(message: Message, state: FSMContext) -> None:
    await support_function.user_tracking.where_who(where=message.text,
                                                   state=state)
    if await support_function.login_test.log_test(message=message,
                                                  state=state):
        msg = await message.answer(text='Бот проектируется для упрощения рабочего процесса Осветительской службы'
                                        ' Михайловского театра!\nС помощью него можно узнать, какой сегодня, или в любой'
                                        ' другой день, спектакль; Узнать каоке количество человек и кто именно работает в'
                                        ' тот или иной день!; Запросить любую выписку и паспорт\nИ МНОГОЕ ДРУГОЕ\n\n'
                                        'В данный момент бот находится в процессе написания, некоторые функции еще'
                                        ' недоступны!\n\nКаждые 5 часов бот удаляет присланные вам файлы!',
                                   reply_markup=main_kb)
        await message.delete()
        await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                                  message_id=msg.message_id,
                                                                  state=state)


@router_start.message(Command(commands=["clear_state_"]))
async def about_bot(message: Message, state: FSMContext) -> None:
    await support_function.user_tracking.where_who(where=message.text,
                                                   state=state)
    await state.clear()
    await message.delete()


@router_start.callback_query()
async def set_user_second_name(callback: CallbackQuery, state: FSMContext) -> None:
    user_data = await state.get_data()
    if callback.data in work_position:
        a_to_table = Position(name=callback.data,
                              employees_id = callback.from_user.id)
        session.add(a_to_table)
        session.commit()
        await state.update_data(login=True)
        msg = await bot.send_message(chat_id=callback.from_user.id,
                                     text='Открываю главное меню!',
                                     reply_markup=main_kb)
        await support_function.delete_pre_message.del_pre_message(chat_id=callback.from_user.id,
                                                                  message_id=msg.message_id,
                                                                  state=state)
    elif 'user_second_name' not in user_data:
        if callback.data in ('Василевский', 'Круссер'):
            await state.update_data(user_second_name='Быкова')
            await callback.answer(text=f'Вы выбрали {callback.data}\nК сожалению вас нет в графике, вы будете'
                                       f' пользоваться ботом под фамилией Быкова',
                                  show_alert=True)
            a_to_table = Employee(id = callback.from_user.id,
                                  last_name = callback.data)
            session.add(a_to_table)
            session.commit()
            msg = await bot.send_message(chat_id=callback.from_user.id,
                                         text='Пожалуйста выберите свою должность!',
                                         reply_markup=choose_work_pos)
            await support_function.delete_pre_message.del_pre_message(chat_id=callback.from_user.id,
                                                                      message_id=msg.message_id,
                                                                      state=state)
        else:
            await callback.answer(text=f'Вы выбрали {callback.data}\nВыбор соответсвующей фамилии напрямую зависит на'
                                       f' корректную работу бота!',
                                  show_alert=True)
            a_to_table = Employee(id=callback.from_user.id,
                                  last_name=callback.data)
            session.add(a_to_table)
            session.commit()
            await state.update_data(user_second_name=callback.data)
            msg = await bot.send_message(chat_id=callback.from_user.id,
                                         text='Пожалуйста выберите свою должность!',
                                         reply_markup=choose_work_pos)
            await support_function.delete_pre_message.del_pre_message(chat_id=callback.from_user.id,
                                                                      message_id=msg.message_id,
                                                                      state=state)