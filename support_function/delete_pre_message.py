from bot import bot, message_id_dict


# функция удаления предыдущего собщения
async def del_pre_message(chat_id, message_id, state) -> None:
    if chat_id not in message_id_dict:
        message_id_dict.update({chat_id: []})
    message_id_dict[chat_id].append(message_id)
    user_data = await state.get_data()
    if "how_del" in user_data:
        how_much_del_pre_message = user_data['how_del']
    else:
        how_much_del_pre_message = 2
    print(len(message_id_dict[chat_id]), how_much_del_pre_message)
    if len(message_id_dict[chat_id]) >= int(how_much_del_pre_message):
        await bot.delete_message(chat_id=chat_id,
                                 message_id=message_id_dict[chat_id].pop(0))
