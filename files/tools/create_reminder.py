#!/usr/bin/env python3
import re

prompt = """
You will help me transalating a query for setting up
a reminder of a certain type to python code. Ask me for
information if you need more.
According to the user request generate python code that consists of the imports to the datetime module,
variable assignments and a dictionary.
Please construct a dictionary named 'job_kwargs' with contains the type of 'trigger' (either an specific date or an interval).
If the trigger is a date the dictionary should contain also the 'run_date' key,
if the trigger is an interval it can have the following keys:
weeks (int), days (int), hours (int), minutes (int), seconds (int) ,start_date (datetime|str), end_date (datetime|str).
Also create an assignment to the variable data consisting of the user content for the reminder.
Only include in your answear code and only the things i asked you for. Do not include commentary text.
Dont enclose your answear with a code snippet nomencalture.
an example of the output required is the following:

import datetime

job_kwargs = {
'trigger': 'interval',
'hours': 1,
'start_date': datetime.datetime.now(),
'end_date': datetime.datetime.now() + datetime.timedelta(days=1)
}

data = 'hello i just wanna check with you'
"""

def parse_and_execute(text):
    match = re.search(r'python\n(.*?)\n', text, re.DOTALL)

    if match:
        return match
    return 'couldntdo what you wanted boss' + text
