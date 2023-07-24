
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

chatbot = ChatBot()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('Received /start command')
    user_id = update.message.from_user.id
    if chatbot.model_type == 'gpt-3.5-turbo-0613':
        chatbot.model_type = 'gpt-4-0613'
    else:
        chatbot.model_type = 'gpt-3.5-turbo-0613'
    bot_res = f"SYSTEM: changed the bot's model to {chatbot.model_type}"
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
    bot_res = chatbot.get_chatbot_response(user_msg, 0, 'public')
    await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_res)

async def echo_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    print(update)
    print(f'User message: {user_msg}')
    try:
        bot_res = chatbot.get_chatbot_response(user_msg, 0, 'private')
    except Exception as e:
        logging.error(f'error {e}', exc_info=True)

    await retry_on_error(context.bot.send_message, 10, 3, chat_id=update.effective_chat.id, text=bot_res)


async def record_all_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    chat_id = message.chat_id
    msg_id = message.message_id
    text = message.text

    print(f"Message ID: {msg_id}")
    print(f"Chat ID: {chat_id}")
    print(f"Text: {text}")

    with open("recorded_messages.txt", "a") as f:
        f.write(f"\nChat ID: {chat_id}, Message ID: {msg_id}, Text: {text}")

if __name__ == '__main__':
    application = ApplicationBuilder().token('931609591:AAHldMP8h6PIAzMkMpLE-NKJIUY3ljX3418').build()
    sc = create_scheduler()
    sc.start()
    ## remove jobs
    #for job in sc.get_jobs():
        #sc.remove_job(job.id)

    #mentioned_filter = filters.create(is_bot_mentioned, name='MentionFilter')

    #record_messages = MessageHandler(filters.TEXT & (~ filters.COMMAND) & (~ filters.Entity('mention')) & (~ filters.ChatType.Private), record_all_messages)
    reply_when_mentioned = MessageHandler(filters.Entity('mention'), reply_when_mentioned)
    echo_private = MessageHandler(filters.ChatType.PRIVATE | filters.Entity('mention'), echo_private)
    start_handler = CommandHandler('gptoggle', start)

    # application.add_handler(record_messages)
    application.add_handler(reply_when_mentioned)
    application.add_handler(start_handler)
    application.add_handler(echo_private)

    application.start_polling()
