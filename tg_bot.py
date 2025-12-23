import logging
import os
from datetime import datetime
from pathlib import Path

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


MENU_TEXT = """
<b>Привет! Это Done — готовая еда прямо из холодильника рядом с офисом.</b>

Бери блюдо всего за 2 минуты: выбери → оплати → открой → разогрей → наслаждайся.

<b>Вот что сейчас есть в меню Done 🍽️:</b>

<b>Номера позиций соответсвуют номеру на полке 😊</b>

<b>🐟 1. Сэндвич с тунцом </b>

Цена: 230 ₽
👉 Оплатить: <a href="https://qr.nspk.ru/BD10003V4S2QT1V38GF8VPEHG9SB4MMP?type=02&bank=100000000004&sum=23000&cur=RUB&crc=DC2A">Ссылка на оплату</a>

<b>🍳 2.Сэндвич с яйцом</b>

Цена: 259 ₽
👉 Оплатить: <a href="https://qr.nspk.ru/AD10007CTK7E754C992RAVQ16CT0772P?type=02&bank=100000000004&sum=25900&cur=RUB&crc=1485">Ссылка на оплату</a>

<b>🐔 3. Онегири с курицей</b>

Цена: 165 ₽
👉 Оплатить: <a href="https://qr.nspk.ru/AD10002SH8DK1Q558QKP5QV24ID8ONUN?type=02&bank=100000000004&sum=16500&cur=RUB&crc=9B8A">Ссылка на оплату</a>

<b>🦐 4. Онегири с креветкой</b>

Цена: 165 ₽
👉 Оплатить: <a href="https://qr.nspk.ru/AD10002SH8DK1Q558QKP5QV24ID8ONUN?type=02&bank=100000000004&sum=16500&cur=RUB&crc=9B8A">Ссылка на оплату</a>

<b>🐔 5. Плов с курицей</b>

Цена: 321 ₽
👉 Оплатить: <a href="https://qr.nspk.ru/BD100073NNBKFVUA837BMTMNA7RMBF94?type=02&bank=100000000004&sum=32100&cur=RUB&crc=111B">Ссылка на оплату</a>

<b>🐷 6. Вок с свининой</b>

Цена: 321 ₽
👉 Оплатить: <a href="https://qr.nspk.ru/BD100073NNBKFVUA837BMTMNA7RMBF94?type=02&bank=100000000004&sum=32100&cur=RUB&crc=111B">Ссылка на оплату</a>

<b>🍴 7. Салат "столичный" </b>

Цена: 235 ₽
👉 Оплатить: <a href="https://qr.nspk.ru/AD10007NARSGHGKL9NIPKPT6BQFT20V0?type=02&bank=100000000004&sum=23500&cur=RUB&crc=E67D">Ссылка на оплату</a>

<b>🐟 8. Салат "сельдь по шубой" </b>

Цена: 211 ₽
👉 Оплатить: <a href="https://qr.nspk.ru/BD10002Q8PI48U6A982Q2GE5AH7O9UAD?type=02&bank=100000000004&sum=21100&cur=RUB&crc=5853">Ссылка на оплату</a>

<b>🫜 9. Салат "винегрет" </b>

Цена: 229 ₽
👉 Оплатить: <a href="https://qr.nspk.ru/BD10001VVSJ4OEFD9NDAHTOGNBRSCML5?type=02&bank=100000000004&sum=22900&cur=RUB&crc=D724">Ссылка на оплату</a>

<b>🔓 Как получить блюдо</b>
1️⃣ Выбери блюдо и нажми на ссылку оплаты.
2️⃣ Оплати — оплата по СПБ.
3️⃣ Бери блюдо, разогревай в микроволновке и получай удовольствие.

💬 Если возник вопрос — напиши прямо сюда - @arseniigolubev.
Мы рядом. 🤗

"""


LOG_FILE = Path("bot_runs.txt")


def log_user_run(update: Update) -> None:
    """Сохраняет информацию о запуске (/start) в текстовый файл."""
    user = update.effective_user
    user_id = user.id if user else "unknown"
    username = user.username or "" if user else ""
    timestamp = datetime.now().isoformat(timespec="seconds")
    line = f"{timestamp}\t{user_id}\t{username}\n"
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    LOG_FILE.open("a", encoding="utf-8").write(line)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Ответ на команду /start: отправляем оформленное меню."""
    log_user_run(update)
    await update.message.reply_html(MENU_TEXT, disable_web_page_preview=True)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """На любое сообщение тоже отправляем меню."""
    await update.message.reply_html(MENU_TEXT, disable_web_page_preview=True)


def main() -> None:
    token = "8553004805:AAHQQs2D-5Nmr64oNCeMdqh23pRDa9ilSe8"
    if not token:
        raise SystemExit("Установите переменную окружения TELEGRAM_BOT_TOKEN")

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    logger.info("Бот запущен. Нажмите Ctrl+C для остановки.")
    application.run_polling()


if __name__ == "__main__":
    main()

