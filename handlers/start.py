import support_function

from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import Router
from keyboards.reply_inline.inline_builder import FamilyInlineKeyboard
from keyboards.reply_markup.reply_builder import MainReplyKeyboard
from sql_data.sql import session, Employee
from loguru import logger

router_start = Router()


@router_start.message(Command(commands=["start"]))
async def start(message: Message, state: FSMContext) -> None:
    """Идентификация пользователя"""

    with session as ses:
        login = ses.query(Employee.id).filter(Employee.id == message.from_user.id).scalar()
    if login is None:
        logger.info(f'Регистрация нового пользователя')
        await state.update_data(user_id=str(message.from_user.id))
        keyboard = await FamilyInlineKeyboard().build()
        msg = await message.answer(text='Пожалуйста, выберите СВОЮ фамилию из списка!',
                                   reply_markup=keyboard.as_markup())
        # Проверяем, обновлялся ли этот стейт через настройки, если да, то не обновляем сейчас
        # обновим user_data чтобы были корректные данные после выбора фамилиим
        user_data: dict = await state.get_data()
        # бесконечный цикл, ждет, пока юсер не нажмет фамилию на клаве, cпим 3 секунды, чтобы меньше гонять цикл и
        # чтобы коллбэк подгрузился
        await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                                  message_id=msg.message_id,
                                                                  state=state)
        await message.delete()
    else:
        logger.info(f'Пользователь с id{login} нажал start')
        await message.delete()
        # Проверяем, обновлялся ли этот стейт через настройки, если да, то не обновляем сейчас
        # Тут на всякий случай, можно будет удалить
        keyboard = MainReplyKeyboard().build()
        msg = await message.answer(text='Вы уже залогинены, приятного общения с ботом!\n/about - тут можно узнать всю'
                                        ' информацию о боте.\n',
                                   reply_markup=keyboard.as_markup())
        await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                                  message_id=msg.message_id,
                                                                  state=state)


@router_start.message(Command(commands=["about"]))
async def about_bot(message: Message, state: FSMContext) -> None:
    """Хэндлер на получение информации о боте"""

    if await support_function.login_test.log_test(message=message):
        keyboard = MainReplyKeyboard().build()
        msg = await message.answer(text='Бот проектируется для упрощения рабочего процесса Осветительской службы'
                                        ' Михайловского театра!\nС помощью него можно узнать, какой сегодня, или в любой'
                                        ' другой день, спектакль; Узнать каоке количество человек и кто именно работает в'
                                        ' тот или иной день!; Запросить любую выписку и паспорт\nИ МНОГОЕ ДРУГОЕ\n\n'
                                        'В данный момент бот находится в процессе написания, некоторые функции еще'
                                        ' недоступны!\n\nКаждые 5 часов бот удаляет присланные вам файлы!',
                                   reply_markup=keyboard.as_markup())
        await message.delete()
        await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                                  message_id=msg.message_id,
                                                                  state=state)


@router_start.message(Command(commands=["__clear_state"]))
async def about_bot(message: Message, state: FSMContext) -> None:
    """Хэндлер разпработчика для отчистки Redis"""

    await state.clear()
    await message.delete()
