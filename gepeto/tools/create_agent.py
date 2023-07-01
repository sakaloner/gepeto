#!/usr/bin/env python3
"""
This is the tool for creating agents by saving them to the database
"""
import json
import re
from database import crud
from utils.functions import parse_json

prompt = """
You are an assitant that will help the user create an agent which whom the user can talk. For this goal you need
to query the user for the following information:
1. The name of the agent.
2. The prompt associated with the agent (this is the text that will program the agent with natural lanugage)
3. The tags associated with this agent (add tags that you consider relevant).
Whenever you have all this information show it to the user and ask for confirmation.
When you get the confirmation from the user output the keyword:
__CREATE_AGENT__:{"name":AGENT_NAME, "prompt":AGENT_PROMPT, "tags":[TAG1,TAG2]}
If the user wants to cancel the procedure output the keword: __CANCEL__
This keywords are only for system use, so the user wont see them.
"""

def parse_and_execute(output):
    if "__CANCEL__" in output:
        print("User cancelled the tool")
    if "__CREATE_AGENT__" in output:
        print("activate the function")
        # We need to import the crud module
        data = parse_json(output)
        res = crud.save_agent(0, data["prompt"], data["name"], data["tags"])
        print("response_crud:",res)
