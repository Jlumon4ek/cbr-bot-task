from aiogram import types
from aiogram import F
from utils.currency import get_currency
from keyboards.inline import currencies



async def RegisterQueryHandler(dp, bot):
    @dp.callback_query(F.data.startswith("CurrencyButton_page_"))
    async def paginate_model_button(query: types.CallbackQuery):
        page = int(query.data.split("_")[-1])
        button = await currencies(page)
        await query.message.edit_reply_markup(reply_markup=button)
        await query.answer()

    @dp.callback_query(F.data.startswith("CurrencyButton_"))
    async def ModelButtonQuery(query: types.CallbackQuery):
        currency_code = query.data.split("_")[-1]

        currency_info = await get_currency(currency_code)
        
        await query.message.answer(
            f"Currency name: {currency_info['name']}\n"
            f"Currency: {currency_info['char_code']}\n"
            f"Vunit rate: {currency_info['vunit_rate']}"
        )
        await query.answer()
