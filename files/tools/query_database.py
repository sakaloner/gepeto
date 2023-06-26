#!/usr/bin/env python3
"""
This is the tool for retrieveing things from the datbase
"""
import json
import re
from database import crud
from utils.functions import parse_json

prompt = """
You are an assistant that can help the user to retrieve
information from the database.
You can help the user to search from three tables: from the message_history table, from the agent table, or the saved data table.
These possibilities are saved in three functions. get_message_history, get_agent and get_saved_data.
you need to first ask the user to choose which function you are going to use.
When you have the function you need to ask the user for more information for the query. The information required would
depend on the function that you chose with the user.
I wiil show you the parameters of each function:
- get_message_history(user_id, period="day"|| "week" || "month", start_date=None, end_date=None)
- get_agent(user_id=None, agent_name=None)
- get_saved_data(user_id=None, tags=None, period=None, start_date=None, end_date=None)
Whenever you have the specific function you will use and its parameters you need output this infomation trough
a dictionary in this way
__CALLING_FUNC__{"function_name":"FUNCTION_CHOSEN", "user_id":"USER_ID", "OTHER_PARAMS":"PARAMS_VALUES"}__
If the user wants to cancel the procedure output the keword: __CANCEL__
These keywords are only for system use, so the user wont see them.
"""

def parse_and_execute(output):
    if "__CANCEL__" in output:
        print("User cancelled the tool")
    if "__CALLING_FUNC__" in output:
        print("activate the function")
        # We need to import the crud module
        data = parse_json(output)
        crud_func = getattr(crud, data['function_name'])

        data.pop('function_name', None)
        if 'user_id' in data:
            data['user_id'] = 0

        res = crud_func(**data)
        print("response_crud:", res)
        return res
