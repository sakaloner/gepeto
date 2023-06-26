
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

    user_entities = update.message.parse_entities(
        [MessageEntity.MENTION, MessageEntity.TEXT_MENTION]
    )
    print('Received private message')
    user_id = update.message.from_user.id
    print(user_id)
    ## If user is not logged in send message for him to login
    # if listapp.get_user_from_db(tl_id=user_id) == None:
    #     print('user not logged in')
    #     user_id = update.message.from_user.id
    #     await context.bot.send_message(
    #         chat_id=update.effective_chat.id,
    #         text=bot_res
    #     )
    #     return

### tests
async def callback_alarm(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id='871787184', text=f'A single message with 30s delay just because: {context.job.data}')
### Main
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
    print(application.job_queue.jobs())
    # (Filters.text & Filters.entity(MENTION))
    # bot_mentioned_handler = MessageHandler(filters.Entity("mention"), bot_mentioned)
    echo_private = MessageHandler(filters.ChatType.PRIVATE | filters.Entity('mention'), echo_private)
    #echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    start_handler = CommandHandler('start', start)


    # application.add_handler(bot_mentioned_handler)
    application.add_handler(start_handler)
    application.add_handler(echo_private)
    #application.add_handler(echo_handler)

    application.run_polling()


# async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     # get entities of the message
#     user_entities = update.message.parse_entities(
#         [MessageEntity.MENTION, MessageEntity.TEXT_MENTION]
#     )
#     # get text of the message
#     text = update.message.text
#     if ('@Parce420Bot' in user_entities.values()):
#         text = update.message.text.replace('@Parce420Bot', '')
#         if (update.message.from_user.id == 871787184):
#             bot_res = get_chatbot_response(text)
#         else:
#             bot_res = get_chatbot_response(text)


#     await context.bot.send_message(
#         chat_id=update.effective_chat.id,
#         #text=bot_res
#         text="this bot is recommending"
#     )

#
