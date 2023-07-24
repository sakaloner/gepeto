#!/usr/bin/env python3
from tools.reminders import create_scheduler, send_message
from database import crud

model_functions = [
    ## Reminder functions
        {
            "name": "set_reminder_date",
            "description": "set a scheduled messages for an specific date",
            "parameters": {
                "type": "object",
                "properties": {
                    "run_date":{
                        "type": "string",
                        "description": "the specific date to send the message"
                    },
                    "message_prompt": {
                        "type": "string",
                        "description": "the goal of the message"
                    }
                },
                "required": ["run_date","message_prompt"],
            },
        },
        {
            "name": "set_reminder_interval",
            "description": "set a scheduled message to run at an specifc interval of time. At least one interval parameter (weeks, days, minutes, seconds) must be provided",
            "parameters": {
                "type": "object",
                "properties": {
                    "message_prompt": {
                        "type": "string",
                        "description":"What is the message for?"
                    },
                    "weeks": {
                        "type": "number",
                        "description":"the interval in weeks for the message repetition"
                    },
                    "days": {
                        "type": "number",
                        "description":"The interval in days for the message repetition"
                    },
                    "minutes": {
                        "type": "number",
                        "description":"The interval in minutes for the message repetition"
                    },
                    "seconds": {
                        "type": "number",
                        "description":"The interval in seconds for the message repetition"
                    },
                    "start_date": {
                        "type": "string",
                        "description":"starting point for the interval calculation"
                    },
                    "end_date": {
                        "type": "string",
                        "description":"latest possible date to trigger sending of the message"
                    },
                },
                "required": ['message_prompt'],
            },
        },
        ## chroma retrieve
        {
            "name": "query_database",
            "description": "retrieve data from the embeddings database",
            "parameters": {
                "type": "object",
                "properties": {
                    "query_string": {
                        "type": "string",
                        "description":"similar string to the data we are looking for"
                    },
                    "direction": {
                        "type": "string",
                        "description":"which entity is the data associated to",
                        "enum": ["assistant","user"]
                    },
                },
                "required": ["query_string"],
            },
        },]
old_functions = [
    ### data base saving
        {
            "name": "save_saved_data",
            "description": "Save general data to the database",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description":"the thing the user wants to save"
                    },
                    "tags": {
                        "type": "array",
                        "description":"an array of strings to use as tags to categorize the saved content, choose them yourself according to the content if the user doesnt provide them",
                        "items": {
                            "type": "string",
                        }
                    },
                },
                "required": ["content","tags"],
            },
        },
        {
            "name": "save_agent",
            "description": "save a new conversational agent/character/chatbot/person to the database",
            "parameters": {
                "type": "object",
                "properties": {
                    "agent_name": {
                        "type":"string",
                        "description":"the name of the agent"
                    },
                    "agent_prompt": {
                        "type": "string",
                        "description":"the text prompt for the agent that will direct its behaviour and output"
                    },
                    "tags": {
                        "type": "array",
                        "description":"an array of strings to use as tags for the agent",
                        "items": {
                            "type": "string",
                        }
                    },
                },
                "required": ["agent_name","agent_prompt","tags"],
            },
        },
    ## database querying
        {
            "name": "get_message_history",
            "description": "find the user message history in a time interval and start and end dates.",
            "parameters": {
                "type": "object",
                "properties": {
                    "period": {
                        "type": "string",
                        "enum": ["day","week","month"],
                        "description":"the period of time in which to search for messages"
                    },
                    "start_date": {
                        "type": "string",
                        "description":"starting point for the interval calculation"
                    },
                    "end_date": {
                        "type": "string",
                        "description":"latest possible date to trigger sending of the message"
                    },
                },
                "required": [],
            },
        },
        {
            "name": "get_agent",
            "description": "query the database for the user saved agents/chatbots/characters/persons",
            "parameters": {
                "type": "object",
                "properties": {
                    "agent_name": {
                        "type": "string",
                        "description":"the name of the agent"
                    },
                },
                "required": [],
            },
        },
        {
            "name": "get_saved_data",
            "description": "query the database for the user saved data",
            "parameters": {
                "type": "object",
                "properties": {
                    "tags": {
                        "type": "array",
                        "items":{
                            "type":"string",
                            "description":"tags that categorize the saved agent"
                        },
                        "description":"keywords to find that might categorize the saved data"
                    },
                    "period": {
                        "type": "string",
                        "enum": ["day","week","month"],
                        "description":"the period on time in wich to make the search for the data"
                    },
                    "start_date": {
                        "type":"string",
                        "description":"the start date for the search"
                    },
                    "end_date":{
                        "type":"string",
                        "description":"the last possible date of time to make the search"
                    }
                },
                "required": [],
            },
        },
    ]

def function_caller(chatbot, f_name, f_args):
    if  "set_reminder" in f_name:
        type_reminder = 'interval' if f_name == 'set_reminder_interval' else 'date'
        message = f_args.pop('message_prompt')
        res = chatbot.get_chatbot_response(message, 0)

        scheduler = create_scheduler()
        scheduler.start()
        scheduler.add_job(send_message, type_reminder, **f_args, args=[res])
        return 1
    elif "query_database" in f_name:
        res = None
        if chatbot.accessType == 'public':
            res = chatbot.chroma.public_col.query(
                query_texts=[f_args["query_string"]],
                where=None,
                n_results=10,
            )
        else:
            res = chatbot.chroma.priv_col.query(
                query_texts=[f_args["query_string"]],
                where=None,
                n_results=10,
            )
        ## make the model choose for the important stuff
        cleaned_res = list(zip(res['ids'], res['documents']))
        paralel = chatbot.interaction_history
        system_msg = """
        This is the response from the function, decide which entries are
        reelvant for the user request
        """
        paralel.append({"role":"system","content":system_msg+str(cleaned_res)})
        return paralel
        bot_res = chatbot.call_model(function_calling="none", history=paralel)
        return bot_res["content"]


    '''
    if f_name == "get_message_history":
        f_args["user_id"] = 0
        ## TODO
        ## Fix that it cant send very long messages
        ## and format them better
        return crud.get_message_history(**f_args)[:10]
    else:
        f_args["user_id"] = 0
        function = getattr(crud, f_name)
        return function(**f_args)
    '''
