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
                    "message": {
                        "type": "string",
                        "description": "the message to send"
                    }
                },
                "required": ["run_date","message"],
            },
        },
        {
            "name": "set_reminder_interval",
            "description": "set a scheduled message to run at an specifc interval of time. At least one interval parameter (weeks, days, minutes, seconds) must be provided",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description":"the message to send"
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
                "required": ['message'],
            },
        },
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

def function_caller(f_name, f_args):
    if  f_name == "set_reminder_interval":
        scheduler = create_scheduler()
        message = f_args.pop('message')
        scheduler.start()
        scheduler.add_job(send_message, 'interval', **f_args, args=[message])
        return 1
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