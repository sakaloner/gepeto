
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
from test_histories import testing

loga = start_logging("tlbot",logging.INFO, "main")

chatbot = ChatBot(testing)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('Received /start command')
    user_id = update.message.from_user.id
    bot_res = f"You said start but i dont give a fuck right now"
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=bot_res
    )

def is_bot_mentioned(update, context):
    bot_username = context.bot.username
    msg_text = update.message.text or ""
    return f"@{bot_username}" in msg_text

async def reply_when_mentioned(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    print('user_msg', user_msg)
    bot_res = chatbot.get_chatbot_response(user_msg, 0)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_res)

async def echo_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    print(update)
    print(f'User message: {user_msg}')
    try:
        bot_res = chatbot.get_chatbot_response(user_msg, 0)
    except Exception as e:
        logging.error(f'error {e}', exc_info=True)

    await retry_on_error(context.bot.send_message, 10, 3, chat_id=update.effective_chat.id, text=bot_res)



if __name__ == '__main__':
    application = ApplicationBuilder().token('931609591:AAHldMP8h6PIAzMkMpLE-NKJIUY3ljX3418').build()
    sc = create_scheduler()
    sc.start()
    ## remove jobs
    for job in sc.get_jobs():
        sc.remove_job(job.id)

    #mentioned_filter = filters.create(is_bot_mentioned, name='MentionFilter')

    reply_when_mentioned = MessageHandler(filters.Entity('mention'), reply_when_mentioned)
    echo_private = MessageHandler(filters.ChatType.PRIVATE | filters.Entity('mention'), echo_private)
    start_handler = CommandHandler('start', start)

    application.add_handler(reply_when_mentioned)
    application.add_handler(start_handler)
    application.add_handler(echo_private)

    application.run_polling()
