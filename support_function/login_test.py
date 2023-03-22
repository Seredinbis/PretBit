from .delete_pre_message import del_pre_message


async def log_test(message, state) -> bool:
    user_data = await state.get_data()
    if 'user_second_name' not in user_data:
        alarm_message = await message.answer(text='Пожалуйста пройдите регистрацию нажав /start')
        await message.delete()
        await del_pre_message(chat_id=alarm_message.chat.id,
                              message_id=alarm_message.message_id,
                              state=state)
        return False
    else:
        return True

