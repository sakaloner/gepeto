#!/usr/bin/env python3
import os
import openai
from dotenv import load_dotenv
import asyncio
import json
import re
import logging
from database import crud
from utils.functions import parse_json, start_logging, get_toolnames

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configure the logger
log = start_logging("chatgpt.py", logging.INFO)

log(f'current pwd {os.getcwd()}')
# Setting up prompting things
first_prompt= """
You are a helpful chinesse sage who uses a lot of emojis
to help an user.
He is your lord and you should refer to the user as "tugo or lord, or your highness or your exelency".
"""


class ChatBot:
  def __init__(self):
    self.tool_mode = False
    self.tool_module = None
    self.tool_name = None
    self.interaction_history = [
      {"role":"system", "content":first_prompt},
    ]
    self.available_tools = get_toolnames('tools/')
    self.metta_prompt = f"Given the tools available ({self.available_tools}) "+ """ do you think you need one of those tools to answear to the user? if so output: __TOOL__:{"tool":"TOOL_NAME"}. Where {TOOL_NAME} is the tool you think is required. If you dont need a tool ignore this past text and answear the user normally."""

  def get_chatbot_response(self, message, tl_id):
    ## dont ask to check if you need a tool while using a tool, although in the future we have to implement it....
    if self.tool_mode:
      content = message
    else:
      content = message + self.metta_prompt

    self.interaction_history.append({"role": "user", "content": content})
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=self.interaction_history,
    )
    crud.save_message(0, message, direction="User")
    response = completion.choices[0].message.content
    log(response)
    crud.save_message(0, response, direction="Assistant")

    if self.tool_mode:
      ## reminder tool
      if self.tool_name == 'create_reminder':
        log('using the reminder tool')
        response = self.tool_module.parse_and_execute(response)
        return (response, response)
      ## parse the response and execute the function if it finds it
      tool_response = self.tool_module.parse_and_execute(response)
      if tool_response:
        self.tool_mode = False
        return response + "tool_response: " + str(tool_response)

    ## is a tool needed?
    if "__TOOL__" in response:
      self.tool_mode = True
      log("a tool is needed")
      self.tool_name = parse_json(response)["tool"]
      log('self.tool_name = ' + self.tool_name)
      ## import the ttol module dynamically
      self.tool_module = __import__(f'tools.{self.tool_name}', fromlist=[''])
      ## use the tool prompt
      if self.tool_name == 'create_reminder':
        self.interaction_history = [{"role": "system", "content":self.tool_module.prompt}]
      else:
        self.interaction_history.append({"role": "system", "content":self.tool_module.prompt})

    return response
