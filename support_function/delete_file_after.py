import asyncio

from bot import bot

files_id_dict = {}


# функция удаления предыдущего собщения c файлом
async def del_files(chat_id, file_id=None, state=None) -> None:
    user_data = await state.get_data()
    if 'how_del_files' in user_data:
        hours = user_data['how_del_files']
    else:
        hours = 3
    if chat_id not in files_id_dict:
        files_id_dict.update({chat_id: []})
    files_id_dict[chat_id].append(file_id)
    # cпим hours часов, потом удаляем файлы
    await asyncio.sleep(3600*int(hours))
    for id_s in files_id_dict[chat_id]:
        if len(files_id_dict[chat_id]) == 0:
            return None
        # добавить отлов ошибки????
        await bot.delete_message(chat_id=chat_id,
                                  message_id=id_s)
        files_id_dict[chat_id].remove(id_s)
