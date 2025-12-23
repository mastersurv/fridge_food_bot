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

from menu_text import MENU_TEXT


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


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
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise SystemExit("Установите переменную окружения TELEGRAM_BOT_TOKEN")

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    logger.info("Бот запущен. Нажмите Ctrl+C для остановки.")
    application.run_polling()


if __name__ == "__main__":
    main()
