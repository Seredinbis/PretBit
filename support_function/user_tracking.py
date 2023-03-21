import datetime


async def where_who(where, state) -> None:
    user = await state.get_data()
    if "user_second_name" in user:
        print(f'{user["user_second_name"]} : {user["user_id"]} in {where} : {datetime.datetime.now()}')
    else:
        print(f'НЕ АВТОРИЗОВАННЫЙ ПОЛЬЗОВАТЕЛЬ НАЖАЛ {where} : {datetime.datetime.now()}')
