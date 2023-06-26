#!/usr/bin/env python3
from telegram import Bot
import asyncio

from pytz import utc

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from datetime import datetime, timedelta

def alarm(time):
    print('Alarm! This alarm was scheduled at %s.' % time)


token = '931609591:AAHldMP8h6PIAzMkMpLE-NKJIUY3ljX3418'
chat_id = '871787184'

async def send_message(msg):
    bot = Bot(token=token)
    await bot.send_message(chat_id=chat_id, text=msg)
    print('message sent')

asyncio.run(send_message('hello btich'))

if __name__ == '__main__':
    sc = AsyncIOScheduler(timezone=utc)
    url = 'sqlite:///database/database.db'
    sc.add_jobstore('sqlalchemy', url=url)

    alarm_time = datetime.now(utc) + timedelta(seconds=10)

    sc.add_job(send_message, 'date', run_date=alarm_time, args=[datetime.now(utc)])

    # start asyncio and scheduler
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    sc.start()

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
