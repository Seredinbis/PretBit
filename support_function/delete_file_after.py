import asyncio

from bot import bot, files_id_dict


# функция удаления предыдущего собщения c файлом
async def del_files(chat_id, file_id=None, files_list=None) -> None:
    if files_list is None:
        if chat_id not in files_id_dict:
            files_id_dict.update({chat_id: []})
        files_id_dict[chat_id].append(file_id)
        # cпим 5 часов, потом удаляем файлы
        await asyncio.sleep(3600*3)
        for id_s in files_id_dict[chat_id]:
            if len(files_id_dict[chat_id]) == 0:
                return None
            # добавить отлов ошибки????
            await bot.delete_message(chat_id=chat_id,
                                     message_id=id_s)
            files_id_dict[chat_id].remove(id_s)
    elif files_list is not None:
        for id_file in files_list:
            await bot.delete_message(chat_id=chat_id,
                                     message_id=id_file)
