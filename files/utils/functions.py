import logging, time, os, re, datetime, time
import json

from typing import *

async def retry_on_error(func, wait=0.1, retry=2, *args, **kwargs):
    i = 0
    while True:
        try:
            return await func(*args, **kwargs)
            break
        except NetworkError:
            logging.exception(f"Network Error. Retrying...{i}")
            i += 1
            await asyncio.sleep(wait)
            if retry != 0 and i == retry:
                break

def start_logging(fname:str, priority) -> Callable:
    """ """
    timestamp = datetime.datetime.now().strftime('%m-%d-%h')

    os.makedirs('logs', exist_ok=True)
    # Configure the logging module
    logging.basicConfig(
        filename=f'logs/main_{timestamp}',  # Specify the filename of the log file
        level=priority,     # Set the logging level to DEBUG, which logs all messages
        format=f'{fname} %(asctime)s %(levelname)s: %(message)s',  # Define the format of the log messages
        datefmt=r'%m-%d-%h',
    )
    # create the logging function
    def log (msg, prio='info'):
        if prio == 'info':
            print(msg)
        types = {
            'debug': logging.debug,
            'info': logging.info,
            'error': logging.error,
        }
        types[prio](msg)
    log(f'started {fname}')
    return log


def parse_json(text):
    # Regular expression pattern that matches { ... }
    pattern = r'\{.*?\}'
    # Search the text for the pattern
    match = re.search(pattern, text)
    # If a match was found
    if match:
        # Get the matched string
        json_string = match.group()
        # Parse the JSON string into a Python dictionary
        data = json.loads(json_string)
        return data
    # If no match was found
    else:
        return None

def get_toolnames(folder_path):
    return [f[:-3] for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and (f != '__init__.py')]
