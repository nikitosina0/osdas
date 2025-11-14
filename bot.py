import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton

from schedule_reader import load_schedule, get_groups, get_days, get_schedule
from config import TOKEN, DAYS

SCHEDULE = load_schedule("data/biophac_schedule.xlsx")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Сохраняем состояние пользователей
user_state = {}  # chat_id -> {"group": None}

def group_keyboard():
    kb = [[KeyboardButton(text=g)] for g in get_groups(SCHEDULE)]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def days_keyboard():
    days = get_days(SCHEDULE)
    kb = [[KeyboardButton(text=d)] for d in days]
    kb.append([KeyboardButton(text="🔙 Выбрать другую группу")])
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! 👋\nВыбери свою группу:", reply_markup=group_keyboard())

@dp.message()
async def handle_message(message: types.Message):
    chat_id = message.chat.id
    text = message.text.strip()

    # Кнопка возврата
    if text == "🔙 Выбрать другую группу":
        user_state.pop(chat_id, None)
        await message.answer("Выбери свою группу:", reply_markup=group_keyboard())
        return

    # Выбор группы
    if chat_id not in user_state:
        if text in get_groups(SCHEDULE):
            user_state[chat_id] = {"group": text}
            await message.answer(f"✅ Группа {text} выбрана!\nТеперь выбери день недели:", reply_markup=days_keyboard())
        else:
            await message.answer("Такой группы нет. Попробуй выбрать из списка.")
        return

    # Выбор дня
    if text in get_days(SCHEDULE):
        group = user_state[chat_id]["group"]
        schedule_text = get_schedule(SCHEDULE, group, text)
        await message.answer(schedule_text)
        return

    # Если что-то непонятное введено
    await message.answer("Не понимаю 😅\nИспользуй кнопки ниже.")

if __name__ == "__main__":
    print("Бот запущен!")
    import asyncio
    asyncio.run(dp.start_polling(bot))
