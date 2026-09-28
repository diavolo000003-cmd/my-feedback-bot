import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

# Данные вашего бота
TOKEN = "8655506909:AAHP7ebhzhNkSnjZRjj1CsGB68RuWNMhYLQ"
ADMIN_ID = 2146440539  

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """Приветствие при нажатии СТАРТ"""
    if message.from_user.id == ADMIN_ID:
        await message.answer("Привет, Илья! Я готов пересылать сообщения пользователей.")
        return

    user_name = html.bold(message.from_user.full_name)
    await message.answer(
        f"Здравствуйте, {user_name}! 👋\n\n"
        f"Оставьте вашу информацию или вопрос прямо здесь. "
        f"Я передам всё Илье, как только он освободится."
    )

@dp.message()
async def feedback_handler(message: Message, bot: Bot) -> None:
    """Пересылка сообщений Илье"""
    if message.from_user.id == ADMIN_ID:
        await message.answer("Илья, чтобы ответить пользователю, напишите ему в его личный чат.")
        return

    user = message.from_user
    user_link = f"tg://user?id={user.id}"
    username_text = f"@{user.username}" if user.username else "отсутствует"
    
    info_header = (
        f"📥 {html.bold('Новое сообщение!')}\n"
        f"👤 Отправитель: <a href='{user_link}'>{html.bold(user.full_name)}</a>\n"
        f"🔗 Юзернейм: {username_text}\n"
        f"✍️ Сообщение:\n\n"
    )
    
    try:
        if message.text:
            await bot.send_message(chat_id=ADMIN_ID, text=info_header + message.text)
        else:
            await bot.send_message(chat_id=ADMIN_ID, text=info_header)
            await message.send_copy(chat_id=ADMIN_ID)
            
    except Exception as e:
        logging.error(f"Ошибка отправки: {e}")

    await message.answer("⌛ Спасибо! Ваша информация принята и передана Илье.")

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
