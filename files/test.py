#!/usr/bin/env python3
"""
Thids is the tool for saving things to the database
"""
import json
import os
import re
from database import crud
from utils.functions import parse_json
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


first_prompt = """
i want to set up a reminder for the 24th of december
According to the following user request generate python code that consists of the imports to the datetime module,
variable assignments and a dictionary.
Please construct a dictionary named 'job_kwargs' with contains the type of 'trigger' (either an specific date or an interval).
If the trigger is a date the dictionary should contain also the 'run_date' key,
if the trigger is an interval it can have the following keys:
weeks (int), days (int), hours (int), minutes (int), seconds (int) ,start_date (datetime|str), end_date (datetime|str).
Also create an assignment to the variable data consisting of the user content for the reminder.
Only include in your answear code and only the things i asked you for. Do not include commentary text.
Dont enclose your answear with a code snippet nomencalture.
The user request is this one:
"""

first_prompt = "hows the weather in boston"

interaction_history = [
    {"role":"system", "content":first_prompt}
]
functions = [
        {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        }
    ]

completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=interaction_history,
    functions=functions,
    function_call="auto"
)
response = completion.choices[0].message.content
print(completion)
