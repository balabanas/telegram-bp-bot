#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import asyncio
from datetime import datetime, time
import logging
import os

from django.conf import settings

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, ApplicationHandlerStop, \
    TypeHandler
from dotenv import load_dotenv

from bot.models import BotUser, Measurement, Schedule

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged


logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

load_dotenv()
ALLOWED_USERS = list(map(int, os.getenv('ALLOWED_USERS').split()))


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


async def check_user(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id not in ALLOWED_USERS:
        bad_user_message = f'Bad user: {update.effective_user.id}'
        await update.effective_message.reply_text(bad_user_message)
        logging.info(bad_user_message)
        raise ApplicationHandlerStop()


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_user_id = update.effective_user.id
    bot_user = await BotUser.objects.aget(tid=telegram_user_id)
    msg_text: str = update.effective_message.text
    figures = tuple(map(int, msg_text.split()))
    sys, dia = figures
    measurement = Measurement(sys=sys, dia=dia)
    measurement.user = bot_user
    await measurement.asave()
    await update.effective_message.reply_text(f"OK {figures}")


async def alarm(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the alarm message."""
    job = context.job
    await context.bot.send_message(job.chat_id, text=f"Beep! {job.data} seconds are over!")


async def set_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add a job to the queue."""
    telegram_user_id = update.effective_user.id
    bot_user = await BotUser.objects.aget(tid=telegram_user_id)

    chat_id = update.effective_message.chat_id
    print(chat_id)
    try:
        # args[0] should contain the time for the timer in seconds
        due: str = context.args[0]
        # if due < 0:
        #     await update.effective_message.reply_text("Sorry we can not go back to future!")
        #     return

        # job_removed = remove_job_if_exists(str(chat_id), context)
        parsed_time = datetime.strptime(due, '%H:%M').time()  # ValueError is possible
        context.job_queue.run_daily(alarm, time=parsed_time, chat_id=chat_id, name=str(chat_id), data=due)  # add tzinfo later

        schedule = Schedule(user=bot_user, time=parsed_time, chat=telegram_user_id)
        await schedule.asave()
        text = "Timer successfully set!"
        # if job_removed:
        #     text += " Old one was removed."
        await update.effective_message.reply_text(text)

    except (IndexError, ValueError):
        await update.effective_message.reply_text("Usage: /set <seconds>")


async def set_scheduler_from_db(app):
    await app.bot.send_message(chat_id='1207815884', text='test, yes!')


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.

    application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()

    job_queue = application.job_queue
    schedules = Schedule.objects.all()
    for schedule in schedules:
        job_queue.run_daily(alarm, time=schedule.time, chat_id=schedule.chat)
    check_user_handler = TypeHandler(Update, check_user)
    message_handler = MessageHandler((filters.TEXT | (filters.PHOTO & filters.CAPTION))
                                     & (~filters.COMMAND), handle_message)


    # on different commands - answer in Telegram
    application.add_handler(check_user_handler, -1)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(message_handler)
    application.add_handler(CommandHandler("set", set_timer))
    # Run the bot until the user presses Ctrl-C
    # asyncio.run(set_scheduler_from_db(application))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
