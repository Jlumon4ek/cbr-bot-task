from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.currency import get_all_currencies

async def currencies(page: int = 1, page_size: int = 5):
    builder = InlineKeyboardBuilder()

    allCurrencies = await get_all_currencies()

    start = (page - 1) * page_size
    end = start + page_size

    for currency in allCurrencies[start:end]:
        builder.row(
            types.InlineKeyboardButton(
                text=f'{currency["char_code"]} - {currency["vunit_rate"]}', callback_data=f"CurrencyButton_{currency['char_code']}"
            )
        )

    total_pages = -(-len(allCurrencies) // page_size)

    builder.row(
        types.InlineKeyboardButton(
            text="<", callback_data=f"CurrencyButton_page_{total_pages if page == 1 else page - 1}"
        ),
        types.InlineKeyboardButton(
            text=f"{page} из {total_pages}", callback_data="ignore"
        ),
        types.InlineKeyboardButton(
            text=">", callback_data=f"CurrencyButton_page_{1 if page == total_pages else page + 1}"
        )
    )

    return builder.as_markup()