#!/usr/bin/env python3

import json
import os
import re
import openai
from dotenv import load_dotenv
import sys




#!/usr/bin/env python3
from telegram import Bot
import asyncio
from pytz import utc
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from datetime import datetime, timedelta

token = '931609591:AAHldMP8h6PIAzMkMpLE-NKJIUY3ljX3418'
chat_id = '871787184'
openai.api_key = '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'

def create_scheduler():
    sc = AsyncIOScheduler(timezone=utc)
    url = 'sqlite:///database/database.db'
    sc.add_jobstore('sqlalchemy', url=url)
    return sc

async def send_message(msg):
    bot = Bot(token=token)
    await bot.send_message(chat_id=chat_id, text=msg)
    print('message sent')





load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

'''
Lo que tengo que hacer es en este file:
- comprobar que funcione el scheduling
  -
- comporar que funcione el scheduling con chatgpt
'''



today_raw = datetime.now(utc)
today = today_raw.strftime("%Y-%m-%d %H:%M:%S")
first_prompt = f"""
today's date is {today}.
i want to set up a reminder every 5 seconds to remember to breath deep.
"""


interaction_history = [
    {"role":"system", "content":first_prompt}
]
functions = [
        {
            "name": "set_reminder_date",
            "description": "set a scheduled messages for an specific date",
            "parameters": {
                "type": "object",
                "properties": {
                    "run_date":{
                        "type": "string",
                        "description": "the specific date to send the message"
                    },
                    "message": {
                        "type": "string",
                        "description": "the message to send"
                    }
                },
                "required": ["run_date","message"],
            },
        },
        {
            "name": "set_reminder_interval",
            "description": "set a scheduled message to run at an specifc interval of time. At least one interval parameter (weeks, days, minutes, seconds) must be provided",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description":"the message to send"
                    },
                    "weeks": {
                        "type": "number",
                        "description":"the interval in weeks for the message repetition"
                    },
                    "days": {
                        "type": "number",
                        "description":"The interval in days for the message repetition"
                    },
                    "minutes": {
                        "type": "number",
                        "description":"The interval in minutes for the message repetition"
                    },
                    "seconds": {
                        "type": "number",
                        "description":"The interval in seconds for the message repetition"
                    },
                    "start_date": {
                        "type": "string",
                        "description":"starting point for the interval calculation"
                    },
                    "start_date": {
                        "type": "string",
                        "description":"latest possible date to trigger sending of the message"
                    },
                },
                "required": ['message'],
            },
        }
    ]

completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=interaction_history,
    functions=functions,
    function_call="auto"
)
response = completion["choices"][0]["message"]

print(completion["choices"])


scheduler = create_scheduler()


if response.get("function_call"):
    f_name = response["function_call"]["name"]
    f_args = json.loads(response["function_call"]["arguments"])

    message = f_args.pop('message')
    if  f_name == "set_reminder_interval":
        scheduler.add_job(send_message, 'interval', **f_args, args=[message])


    
    print(f_name,f_args)

if __name__ == '__main__':
    asyncio.run(send_message('hello there'))
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    scheduler.start()

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass

