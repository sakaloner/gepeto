#!/usr/bin/env python3
from telegram import Bot
import asyncio
from pytz import utc
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from datetime import datetime, timedelta

token = '931609591:AAHldMP8h6PIAzMkMpLE-NKJIUY3ljX3418'
chat_id = '871787184'

async def send_message(msg):
    bot = Bot(token=token)
    await bot.send_message(chat_id=chat_id, text=msg)
    print('message sent')

def create_scheduler():
    sc = AsyncIOScheduler(timezone=utc)
    url = 'sqlite:///database/database.db'
    sc.add_jobstore('sqlalchemy', url=url)
    return sc

if __name__ == '__main__':
    scheduler = create_scheduler()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    scheduler.start()
    print(scheduler.get_jobs())
    scheduler.print_jobs()
    scheduler.remove_job('e02de003c1e34d38aa15a5008ffc7266')

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
