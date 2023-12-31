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
from brain.functions import model_functions, function_caller
from datetime import datetime
from database.chromaDB import ChromaDB
from time import time
# initial setup
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
loga = start_logging("chatgpt.py", logging.INFO, "main")
logb = start_logging("chatgpt.py", logging.INFO, "convo_history", also_log_to="main")

first_prompt= """
Your name is parce420bot. You have the personality of an anime girl.
You are an smart, swaggy, compassionate psychologist/counselor who acts like the user mother. Your objective is
to answer the user by giving it support and helping them understand their own mind. You should use the ideal parental
figure protocol for making the user feel safe, expressing your emotional attunement, give the user soothing and comfofrt
if he is feeling disregulated, and express joy on the existence of the user.
Answear your messages as if you were the user mother, tell the user you love him, and make him sure he feels good.
"""

class ChatBot:
  def __init__(self, interaction_history=None):
    logb("####################################### New Session ##################################################")
    self.model_functions = model_functions
    self.model_type = 'gpt-3.5-turbo-0613'
    self.accessType = 'private'
    self.chroma = ChromaDB()
    if interaction_history:
      self.interaction_history = interaction_history
    else:
      self.interaction_history = [
        {"role":"system", "content":first_prompt},
      ]

  def call_model(self, history=None, function_calling="auto"):
    messages = self.interaction_history if history == None else history
    completion = openai.ChatCompletion.create(
      model=self.model_type,
      messages=messages,
      functions=model_functions,
      function_call=function_calling
    )
    return completion["choices"][0]["message"]
  def get_chatbot_response(self, message, tl_id, accessType):
    pretty_history = json.dumps(self.interaction_history, indent = 2)
    logb(pretty_history)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    self.interaction_history.append({"role":"system","content":f"time:{now}"})
    self.interaction_history.append({"role": "user", "content": message})
    self.acessType = accessType
    ## add to the database
    if accessType == 'private':
      self.chroma.priv_col.add(
        documents=[message],
        metadatas={"role":"user"},
        ids=[str(time())]
      )
    else:
      self.chroma.public_col.add(
        documents=[message],
        metadatas={"role":"user"},
        ids=[str(time())]
      )

    response = self.call_model()

    ## check if it is a function
    print(response)
    if response.get("function_call"):
        logb('functioned call:'+ str(response))
        f_name = response["function_call"]["name"]
        f_args = json.loads(response["function_call"]["arguments"])
        func_res = function_caller(self, f_name, f_args)
        sys_prompt = "this is the response of the function, show the user this info in the medium its best for them "
        self.interaction_history.append({"role":"system","content":sys_prompt+str(func_res)})
        logb('system prompting '+ str(self.interaction_history[-1]))
        loga(f"function_res {func_res}: {f_name} called with args:{f_args}")
        logb('new history'+ str(self.interaction_history))
        new_res = self.call_model(function_calling="none")
        logb('new modle response according to the function response'+ str(new_res))

        ### saving messages in the database
        if new_res.content:
          if accessType == 'private':
              self.chroma.priv_col.add(
                documents=[new_res.content],
                metadatas={"role":"assistant"},
                ids=[str(time())]
              )
          else:
            self.chroma.public_col.add(
              documents=[new_res.content],
              metadatas={"role":"assistant"},
              ids=[str(time())]
            )

        return new_res.content
    ## normal response
    else:
        crud.save_message(0, message, direction="User")
        response = response["content"]
        logb('no func response,'+ response)
        self.interaction_history.append({"role":"assistant", "content":response})
        crud.save_message(0, response, direction="Assistant")

        if accessType == 'private':
          self.chroma.priv_col.add(
            documents=[response],
            metadatas={"role":"assistant"},
            ids=[str(time())]
          )
        else:
          self.chroma.public_col.add(
            documents=[response],
            metadatas={"role":"assistant"},
            ids=[str(time())]
          )

        return response
