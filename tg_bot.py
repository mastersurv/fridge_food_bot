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

ALLOWED_USERNAMES = os.getenv(
    "ALLOWED_USERNAMES", "arseniigolubev"
).split(",")


def is_user_allowed(username: str | None) -> bool:
    """Проверяет, есть ли пользователь в списке разрешенных."""
    if not username:
        return False
    return username.lower().strip() in [
        u.lower().strip() for u in ALLOWED_USERNAMES
    ]


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


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет файл bot_runs.txt только разрешенным пользователям."""
    user = update.effective_user
    username = user.username if user else None

    if not is_user_allowed(username):
        await update.message.reply_text(
            "❌ У вас нет доступа к этой команде."
        )
        return

    if not LOG_FILE.exists():
        await update.message.reply_text(
            "📄 Файл статистики пока пуст."
        )
        return

    try:
        with LOG_FILE.open("rb") as file:
            await update.message.reply_document(
                document=file,
                filename="bot_runs.txt",
                caption="📊 Статистика запусков бота",
            )
    except Exception as e:
        logger.error(f"Ошибка при отправке файла: {e}")
        await update.message.reply_text(
            "❌ Ошибка при отправке файла статистики."
        )


def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise SystemExit("Установите переменную окружения TELEGRAM_BOT_TOKEN")

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    )

    logger.info("Бот запущен. Нажмите Ctrl+C для остановки.")
    application.run_polling()


if __name__ == "__main__":
    main()
