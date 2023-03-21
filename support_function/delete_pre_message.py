from bot import bot, message_id_dict


# функция удаления предыдущего собщения
async def del_pre_message(chat_id, message_id, state) -> None:
    if chat_id not in message_id_dict:
        message_id_dict.update({chat_id: []})
    message_id_dict[chat_id].append(message_id)
    user_data = await state.get_data()
    if "how_much_del_pre_message" in user_data:
        how_much_del_pre_message = user_data["how_much_del_pre_message"]
    else:
        how_much_del_pre_message = 2
    if len(message_id_dict[chat_id]) == how_much_del_pre_message:
        await bot.delete_message(chat_id=chat_id,
                                 message_id=message_id_dict[chat_id].pop(0))
