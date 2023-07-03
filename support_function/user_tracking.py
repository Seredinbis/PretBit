import datetime
from bot import user_track

async def where_who(where, state) -> None:
    user = await state.get_data()
    if "user_second_name" in user:
        user_track.append(f'{user["user_second_name"]} : {user["user_id"]} in {where} : {datetime.datetime.now()}\n')
    else:
        user_track.append(f'НЕ АВТОРИЗОВАННЫЙ ПОЛЬЗОВАТЕЛЬ НАЖАЛ {where} : {datetime.datetime.now()}\n')
