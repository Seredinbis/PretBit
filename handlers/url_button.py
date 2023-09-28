from aiogram.filters import Text
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import Router
from keyboards.reply_markup.main import main_kb
import support_function


router_url = Router()


# обработка кнопки 'Ссылки'в главном меню
@router_url.message(Text('Ссылки'))
async def get_url(message: Message, state: FSMContext) -> None:
    await support_function.user_tracking.where_who(where=message.text,
                                                   state=state)
    if await support_function.login_test.log_test(message=message):
        msg = await message.answer(text='[Михайловский театр](https://mikhailovsky.ru/)'
                                        '\n[lee](https://leefilters.com/lighting/colour-effect-lighting-filters/)'
                                        '\n[rosco](https://us.rosco.com/en/products/family/filters-and-diffusions)'
                                        '\n[clay paky](https://www.claypaky.it/en/products/entertainment)'
                                        '\n[herь kakaяto](https://www.lightingschool.eu/knowledge-center/)',
                                   reply_markup=main_kb,
                                   disable_web_page_preview=True,
                                   parse_mode='Markdown')
        await state.update_data(whitch_kb_was='main_kb')
        await message.delete()
        await support_function.delete_pre_message.del_pre_message(chat_id=msg.chat.id,
                                                                  message_id=msg.message_id,
                                                                  state=state)
