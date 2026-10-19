import asyncio
import logging
import random

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# Telegram Bot Token
BOT_TOKEN = "8708701449:AAEruPnv6Xi3wIKAcCalWZvg66oVfcghTdM"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

# UNO Karta ma'lumotlari
UNO_COLORS = ["🔴 Qizil", "🔵 Moviy", "🟢 Yashil", "🟡 Sariq"]
UNO_VALUES = [
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "Skip 🚫",
    "Reverse 🔄",
    "Draw +2 ➕2️⃣",
]

# 🔘 DOIMIY TUGMALAR (REPLY KEYBOARD)
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎴 UNO Karta tortish")],
        [
            KeyboardButton(text="🎲 Tasodifiy son"),
            KeyboardButton(text="❓ Yordam"),
        ],
    ],
    resize_keyboard=True,
)


@dp.message(Command("start"))
async def start_handler(message: types.Message):
    user_name = message.from_user.first_name
    await message.answer(
        f"Salom {user_name}! Botga xush kelibsiz.\n\n"
        f"Kerakli menyuni tanlash uchun pastdagi tugmalardan foydalaning:",
        reply_markup=main_keyboard,
    )


@dp.message(Command("help"))
@dp.message(lambda msg: msg.text == "❓ Yordam")
async def help_handler(message: types.Message):
    await message.answer(
        "📌 Bot buyruqlari ro'yxati:\n"
        "1. /start - Botni qayta ishga tushirish\n"
        "2. 🎴 UNO Karta tortish - Tasodifiy UNO kartasini olish\n"
        "3. 🎲 Tasodifiy son - 1 dan 100 gacha son tanlash\n"
    )


# 🎴 UNO MINI GAME HANDLER
@dp.message(lambda msg: msg.text == "🎴 UNO Karta tortish" or msg.text == "/uno")
async def uno_handler(message: types.Message):
    user_name = message.from_user.first_name

    # 10% ehtimollik bilan Wild +4 kartasi tushadi
    if random.randint(1, 10) == 1:
        await message.reply(
            f"👑 **Omadli yurish, {user_name}!**\n\n"
            f"🃏 Sizga **BLACK WILD +4 👑** kartasi tushdi!\n"
            f"💥 Qolgan barcha o'yinchilar +4 ta karta oladi!"
        )
    else:
        color = random.choice(UNO_COLORS)
        value = random.choice(UNO_VALUES)
        await message.reply(
            f"🎴 **{user_name} kartani tortdi:**\n\n"
            f"Karta: **{color} {value}**"
        )


# 🎲 TASODIFIY SON FUNKSIYASI
@dp.message(lambda msg: msg.text == "🎲 Tasodifiy son")
async def random_number_handler(message: types.Message):
    number = random.randint(1, 100)
    await message.reply(f"🎲 Sizning tasodifiy soningiz: **{number}**")


# 💬 ODDITY MATNLI XABARLARNI QAYTA ISHLASH
@dp.message()
async def process_chat_handler(message: types.Message):
    text = message.text.lower()

    if "salom" in text or "qalesiz" in text:
        await message.reply("Salom! Ishlaringiz yaxshimi?")
    elif "yaxshi" in text:
        await message.reply("Juda soz!")
    else:
        await message.reply(f"Siz yubordingiz: {message.text}")


async def main():
    print("Bot muvaffaqiyatli ishga tushdi...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())