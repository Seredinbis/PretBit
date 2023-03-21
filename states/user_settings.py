from aiogram.fsm.state import State, StatesGroup


# пользовательские настройки Юсер id и секнод нейм устанавливаем на команде /start
class UserSettings(StatesGroup):
    user_id: str = State()
    user_second_name: str = State()
    login: bool = State()
    user_working_position: str = State()
    auto_send: str = State()
    time_auto_send: str = State()
    whitch_kb_was: str = State()
    genre: str = State()
    show: str = State()
    what: str = State()
    how_much_del_pre_message: int = State()
    set_dpm: bool = State()
    url_id: dict = State()
