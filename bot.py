from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import db_handler as handler
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


"""Information command"""


@dp.message_handler(commands=['start'])  # works
async def send_welcome(message: types.Message):
    await bot.send_message(message.from_user.id, "Bot is ready to work!\n"
                                                 "Have a lucky shift, {0.first_name}!\n"
                                                 "Please, read it /help".format(message.from_user))


@dp.message_handler(commands=['help'])  # works
async def send_welcome(message: types.Message):
    await message.answer(
        "Commands for waiters and admins:\n"
        "Add order to (table) (amount) (drink)\n"
        "Delete table(table)\n"
        "Delete from (table) (drink)\n"
        "Bill (table)\n\n"
        
        "Commands only for admin:\n"
        "Add to store (amount) (name)\n"
        "Store minus (amount) (name)\n"
        "Store plus (amount) (name)\n"
        "Delete from store (name)\n\n\n"
        
        "Cheat sheet, or examples:\n"
        "table: 001, 012, 777\n"
        "drinks: Daiquiri, Gin Tonic\n"
        "name: house_gin, water, lime\n"
        "amount: 1.2, 1.0, 001, 012")


"""Command to add order"""


@dp.message_handler(lambda message: message.text.startswith('Add order to'))  #
async def add_order(message: types.Message):
    row_table = message.text[13:16]
    row_amount = message.text[17:20]
    row_drink = message.text[21:]
    handler.add_order(int(row_table), row_drink, int(row_amount))
    await message.answer(f"You've ordered {row_amount} {row_drink} to table #{row_table}")


"""Commands to edit store"""


@dp.message_handler(lambda message: message.text.startswith('Delete from store'))  # works
async def del_table(message: types.Message):
    row_name = message.text[18:]
    handler.delete_from_store(row_name)
    await message.answer(f"You have already deleted {row_name} from store.")


@dp.message_handler(lambda message: message.text.startswith('Add to store'))  # works
async def del_table(message: types.Message):
    row_amount = float(message.text[13:16])
    row_name = message.text[17:]
    handler.add_store(row_name, row_amount)
    await message.answer(f"You have already added {row_amount} {row_name} to store.")


@dp.message_handler(lambda message: message.text.startswith('Store plus'))  # works
async def del_table(message: types.Message):
    row_amount = float(message.text[11:14])
    row_name = message.text[15:]
    handler.store_subjoin(row_name, row_amount)
    await message.answer(f"{row_amount} {row_name} was subjoined to store.")


@dp.message_handler(lambda message: message.text.startswith('Store minus'))  # works
async def del_table(message: types.Message):
    row_amount = float(message.text[12:15])
    row_name = message.text[16:]
    handler.store_subtract(row_name, row_amount)
    await message.answer(f"{row_amount} {row_name} was subtracted from store.")


"""Commands for edit guest's table"""


@dp.message_handler(lambda message: message.text.startswith('Delete from'))  # works
async def del_table(message: types.Message):
    row_id = int(message.text[12:15])
    row_drink = message.text[16:]
    handler.del_from_gtable(row_id, row_drink)
    await message.answer(f"From table #{row_id} was deleted all {row_drink}.")


@dp.message_handler(lambda message: message.text.startswith('Delete table'))  # works
async def del_table(message: types.Message):
    row_id = int(message.text[12:16])
    handler.del_gtable(row_id)
    await message.answer(f"Table #{row_id} was deleted.")


"""Command to get a bill"""


@dp.message_handler(lambda message: message.text.startswith('Bill'))  # works, but doesn't show the bill for user
async def del_table(message: types.Message):
    row_id = int(message.text[5:8])
    handler.get_bill(row_id)
    await message.answer(f"The bill for table #{row_id} is printed.")


if __name__ == '__main__':
    executor.start_polling(dp)
