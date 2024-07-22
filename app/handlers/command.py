from aiogram import types
from aiogram.filters.command import Command
from utils.currency import get_currency
from keyboards.inline import currencies

async def register_command_handlers(dp, bot):
    @dp.message(Command("start"))
    async def start(message: types.Message):
        username = message.from_user.username
        await message.answer(f"Hello! {username}. I'm a bot!")
    
    @dp.message(Command("rates"))
    async def rates(message: types.Message):
        await message.answer("Fetching exchange rates...")
        await message.answer('Exchange rates are fetched!', reply_markup=await currencies())

    @dp.message(Command("exchange"))
    async def exchange(message: types.Message):
        parts = message.text.split()
        if len(parts) < 4:
            await message.answer("Usage: /exchange <from_currency> <to_currency> <amount>")
            return

        _, from_currency, to_currency, amount_str = parts
        if not amount_str.isdigit():
            await message.answer("Amount should be a number.")
            return

        currency_info = await get_currency(from_currency)

        if currency_info is None:
            await message.answer(f"Currency {from_currency} not found")
            return
        
        currency_price = currency_info['vunit_rate']
        if currency_price is None:
            await message.answer(f"Currency {from_currency} is not convertible")
            return
    
        amount = int(amount_str)

        converted_amount = amount * currency_price
        await message.answer(f"{amount} {from_currency} = {converted_amount} {to_currency}")

