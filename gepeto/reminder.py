#!/usr/bin/env python3
import os
import re
from telegram import Bot
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from tools.reminders import create_scheduler


if __name__ == '__main__':
    scheduler = create_scheduler()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    scheduler.start()
    scheduler.print_jobs()

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
