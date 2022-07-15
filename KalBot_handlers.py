import aiogram
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import Excel
import State
import config
import filter
from main import bot


async def admin_not():
    await bot.send_message(config.ADMIN_ID, "Бот запущен!")


async def start(message: aiogram.types.Message):
    await message.answer(f'Приветствую, {message.from_user.full_name}!')
    await message.answer('Я рассчитываю калорийную стоимость вашего блюда. Для моей работы необходимо знать ингредиенты и массу. \n\nДля начала напишите /kalory. \nДля остановки напишите /stop.')


async def stop(message: aiogram.types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Процесс остановлен.")


async def kalory_1(message: aiogram.types.Message):
    await message.answer("Введите название продукта, а я посмотрю, есть ли он у меня в базе.")
    await State.StateKalory.St1.set()


async def kalory_2(message: aiogram.types.Message, state: FSMContext):
    text = message.text
    res = Excel.ProductSearch(text)
    if res == "Ничего похожего не нашлось(":
        await message.answer("Такого продукта у нас нет!")
        await kalory_1(message)
    else:
        await state.update_data(a=res)
        data = await state.get_data()
        data = data.get("a")
        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for i in data:
            btn = KeyboardButton(i[0])
            kb.add(btn)
        await message.answer("Удалось найти такие варианты.", reply_markup=kb)
        await State.StateKalory.St2.set()


async def kalory_3(message: aiogram.types.Message, state: FSMContext):
    text = message.text
    data = await state.get_data()
    data = data.get("a")
    mark = False
    for i in data:
        if i[0] == text:
            await state.update_data(b=i)
            mark = True
            break
    if not mark:
        await message.answer("Такого продукта у нас нет!")
        await kalory_1(message)
    else:
        await State.StateKalory.St3.set()
        await message.answer("Введите вес в граммах.")

async def error(message: aiogram.types.Message):
    await message.answer("Вы ввели не число, попробуйте еще раз.")


async def kalory_4(message: aiogram.types.Message, state: FSMContext):
    data_0 = await state.get_data()
    data_b = data_0.get("b")
    val = data_b[1]
    prod = data_b[0]
    sum = int(message.text) * val / 100
    arr = [prod, val, sum]
    if "d" in data_0:
        data = data_0.get("d")
        data.append(arr)
        await state.update_data(d=data)
    else:
        await state.update_data(d=[arr])
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btnyes = KeyboardButton("Да")
    btnno = KeyboardButton("Нет")
    kb.add(btnyes).add(btnno)
    await message.answer("Есть ли еще другие продукты?", reply_markup=kb)
    await State.StateKalory.St4.set()


async def kalory_5(message: aiogram.types.Message, state: FSMContext):
    text = message.text
    if text == "Да":
        await State.StateKalory.St5.set()
        await kalory_1(message)
    elif text == "Нет":
        data = await state.get_data()
        data = data.get("d")
        res = ""
        val = 0
        for i in data:
            res += i[0] + " - \t" + f"<i>{str(round(i[2], 1))}</i>" + " ккал\n\n"
            val += round(i[2], 1)
        res += "<b>\nВсего - \t</b>" + f"<i>{str(round(val, 1))}</i>" + " ккал"
        await message.answer(res, parse_mode='HTML')
        await state.finish()


def reg_start(dp: aiogram.Dispatcher):
    dp.register_message_handler(start, commands='start')

def reg_stop(dp: aiogram.Dispatcher):
    dp.register_message_handler(stop, commands='stop')

def reg_kalory_1(dp: aiogram.Dispatcher):
    dp.register_message_handler(kalory_1, commands='kalory')

def reg_kalory_2(dp: aiogram.Dispatcher):
    dp.register_message_handler(kalory_2, state=State.StateKalory.St1)

def reg_kalory_3(dp: aiogram.Dispatcher):
    dp.register_message_handler(kalory_3, state=State.StateKalory.St2)

def reg_kalory_4(dp: aiogram.Dispatcher):
    dp.register_message_handler(kalory_4, filter.IsDigit(), state=State.StateKalory.St3)

def reg_kalory_5(dp: aiogram.Dispatcher):
    dp.register_message_handler(kalory_5, state=State.StateKalory.St4)

def reg_error(dp: aiogram.Dispatcher):
    dp.register_message_handler(error, state=State.StateKalory.St3)

