"""
This is the tool for saving things to the database
"""
import json
import re
from database import crud
from utils.functions import parse_json
from utils.functions import start_logging

prompt = """
You are an assistant that can help the user to save things to the database
You can help the user to save things to two tables:agent, or saved data.
These possibilities are saved in three functions. save_agent, save_saved_data.
you need to first ask the user to choose which function you are going to use.
When you have the function you need to ask the user for more information. The information required would
depend on the function that you chose with the user.
I wiil show you the parameters for each function:
- save_saved_data(user_id, content, tags):
- save_agent(user_id, agent_prompt, agent_name=None, tags)

Whenever you have the specific function you will use and its parameters you need output this infomation trough
a dictionary in this way
__CALLING_FUNC__{"function_name":"FUNCTION_CHOSEN", "user_id":"USER_ID", "OTHER_PARAMS":"PARAMS_VALUES"}
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
        print("response_crud:",res)
        return res
