#!/usr/bin/env python3
import os
import re
from telegram import Bot
import asyncio
from pytz import utc
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from datetime import datetime, timedelta

from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TLBOT_API_KEY")
chat_id = '871787184'

def create_scheduler():
    sc = AsyncIOScheduler(timezone=utc)
    url = 'sqlite:///database/database.db'
    sc.add_jobstore('sqlalchemy', url=url)
    return sc

async def send_message(msg):
    bot = Bot(token=token)
    await bot.send_message(chat_id=chat_id, text=msg)
    print('message sent')

