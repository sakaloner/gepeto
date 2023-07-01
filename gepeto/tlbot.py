
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, MessageEntity
from telegram.ext import InlineQueryHandler, ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler
from utils.functions import retry_on_error, start_logging
from brain.chatgpt import ChatBot
from database import crud
from telegram.error import NetworkError
import datetime
import asyncio
import logging
import pytz

from tools.reminders import create_scheduler, send_message

log = start_logging("tlbot",logging.INFO)

chatbot = ChatBot()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('Received /start command')
    user_id = update.message.from_user.id
    bot_res = f"You said start but i dont give a fuck right now"
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=bot_res
    )
async def echo_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    print(f'User message: {user_msg}')
    try:
        crud.save_message(0, user_msg, direction="User")
        bot_res = chatbot.get_chatbot_response(user_msg, 0)

        crud.save_message(0, bot_res, direction="Assistant")

    except Exception as e:
        logging.error(f'error {e}', exc_info=True)

    await retry_on_error(context.bot.send_message, 10, 3, chat_id=update.effective_chat.id, text=bot_res)



if __name__ == '__main__':
    application = ApplicationBuilder().token('931609591:AAHldMP8h6PIAzMkMpLE-NKJIUY3ljX3418').build()
    sc = create_scheduler()
    sc.start()
    ## remove jobs
    #for job in sc.get_jobs():
        #sc.remove_job(job.id)

    echo_private = MessageHandler(filters.ChatType.PRIVATE | filters.Entity('mention'), echo_private)
    start_handler = CommandHandler('start', start)

    application.add_handler(start_handler)
    application.add_handler(echo_private)

    application.run_polling()
