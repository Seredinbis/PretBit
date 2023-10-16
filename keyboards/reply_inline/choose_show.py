from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton, InlineKeyboardBuilder
from disk_api.yandex_d import Chain, Manual

bo1 = InlineKeyboardButton(text='Аида', callback_data='Аида')
bo2 = InlineKeyboardButton(text='Волшебная флейта', callback_data='Волшебная флейта')
bo3 = InlineKeyboardButton(text='Иоланта (Жолдак)', callback_data='Иоланта (Жолдак)')
bo4 = InlineKeyboardButton(text='Манон Леско', callback_data='Манон Леско')
bo5 = InlineKeyboardButton(text='Опричник', callback_data='Опричник')
bo6 = InlineKeyboardButton(text='Пиковая дама', callback_data='Пиковая дама')
bo7 = InlineKeyboardButton(text='Севильский Цирюльник', callback_data='Севильский Цирюльник')
bo8 = InlineKeyboardButton(text='Сельская честь', callback_data='Сельская честь')
bo9 = InlineKeyboardButton(text='Тоска', callback_data='Тоска')
bo10 = InlineKeyboardButton(text='Травиата', callback_data='Травиата')
bo11 = InlineKeyboardButton(text='Фигаро', callback_data='Фигаро')
bo12 = InlineKeyboardButton(text='Золушка', callback_data='Золушка')
bo13 = InlineKeyboardButton(text='Иоланта', callback_data='Иоланта')
bo14 = InlineKeyboardButton(text='Летучий Голландец', callback_data='Летучий Голландец')
bo15 = InlineKeyboardButton(text='Назад', callback_data='Назад к выбору жанра')
bo16 = InlineKeyboardButton(text='Вернуться в главное меню', callback_data='Вернуться в главное меню')

choose_opera_kb = InlineKeyboardMarkup(inline_keyboard=[[bo1], [bo2], [bo3], [bo4], [bo5], [bo6], [bo7], [bo8], [bo9],
                                                        [bo10], [bo11], [bo12], [bo13], [bo14], [bo15], [bo16]])


bb1 = InlineKeyboardButton(text='Баядерка', callback_data='Баядерка')
bb2 = InlineKeyboardButton(text='Дон Кихот', callback_data='Дон Кихот')
bb3 = InlineKeyboardButton(text='Дуато', callback_data='Дуато')
bb4 = InlineKeyboardButton(text='Жизель', callback_data='Жизель')
bb5 = InlineKeyboardButton(text='Золушка', callback_data='Золушка')
bb6 = InlineKeyboardButton(text='Конек Горбунок', callback_data='Конек Горбунок')
bb7 = InlineKeyboardButton(text='Коппелия', callback_data='Коппелия')
bb8 = InlineKeyboardButton(text='Корсар', callback_data='Корсар')
bb9 = InlineKeyboardButton(text='Лауренсия', callback_data='Лауренсия')
bb10 = InlineKeyboardButton(text='Лебединое Озеро', callback_data='Лебединое Озеро')
bb11 = InlineKeyboardButton(text='Пламя парижа', callback_data='Пламя парижа')
bb12 = InlineKeyboardButton(text='Ромео И Дж', callback_data='Ромео И Дж')
bb13 = InlineKeyboardButton(text='Сильфида', callback_data='Сильфида')
bb14 = InlineKeyboardButton(text='Спартак', callback_data='Спартак')
bb15 = InlineKeyboardButton(text='Спящая Красавица', callback_data='Спящая Красавица')
bb16 = InlineKeyboardButton(text='Тщетная предосторожность', callback_data='Тщетная предосторожность')
bb17 = InlineKeyboardButton(text='Чиполлино', callback_data='Чиполлино')
bb18 = InlineKeyboardButton(text='Щелкунчик', callback_data='Щелкунчик')
bb19 = InlineKeyboardButton(text='балеты Васильева', callback_data='балеты Васильева')
bb20 = InlineKeyboardButton(text='Назад', callback_data='Назад к выбору жанра')
bb21 = InlineKeyboardButton(text='Вернуться в главное меню', callback_data='Вернуться в главное меню')

choose_balet_kb = InlineKeyboardMarkup(inline_keyboard=[[bb1], [bb2], [bb3], [bb4], [bb5], [bb6], [bb7], [bb8], [bb9],
                                                        [bb10], [bb11], [bb12], [bb13], [bb14], [bb15], [bb16], [bb17],
                                                        [bb18], [bb19], [bb20], [bb21]])

choose_lebedki_kb = InlineKeyboardBuilder()
for show in Chain().get_folders():
    choose_lebedki_kb.row(InlineKeyboardButton(text=show['name'],
                                               callback_data=f'ЛЕБЕДКИ {show["name"]}'))
choose_lebedki_kb.row(InlineKeyboardButton(text='Назад',
                                           callback_data='Назад к выбору жанра'))
choose_lebedki_kb.row(InlineKeyboardButton(text='Вернуться в главное меню',
                                           callback_data='Вернуться в главное меню'))

choose_manual_kb = InlineKeyboardBuilder()
for show in Manual().get_folders():
    choose_manual_kb.row(InlineKeyboardButton(text=show['name'],
                                              callback_data=f'МАНУАЛ {show["name"]}'))
choose_manual_kb.row(InlineKeyboardButton(text='Назад',
                                          callback_data='Назад к выбору жанра'))
choose_manual_kb.row(InlineKeyboardButton(text='Вернуться в главное меню',
                                          callback_data='Вернуться в главное меню'))
