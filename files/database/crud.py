from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import json
from database import models
from database import main
from sqlalchemy import select
from sqlalchemy.sql import insert
### Load stuff
# Load env variables
load_dotenv()
url = os.environ.get('MAIN_URL')
# check connection with psql db
db = main.SessionLocal()

models.Base.metadata.create_all(bind=main.engine)

# Add a message to the history
def save_message(user_id, message, direction):
    msg = models.Message_history(
        user_id=user_id,
        message=message,
        direction=direction
    )
    db.add(msg)
    db.commit()
    return "Added succesfully"

def save_agent(user_id, agent_prompt, agent_name, tags):
    # Create a new Agent object
    new_agent = models.Agent(
        user_id=user_id,
        agent_prompt=agent_prompt,
        agent_name=agent_name
    )

    # Add the new Agent object to the session
    db.add(new_agent)
    db.flush()

    # For each tag in the list of tags
    for tag_name in tags:
        # Query the Tag table to see if this tag already exists
        tag = db.query(models.Tag).filter(models.Tag.tag == tag_name).first()

        # If the tag doesn't exist, create a new one
        if tag is None:
            tag = models.Tag(tag=tag_name)
            db.add(tag)
            db.flush()

        # Create a new AgentTag linking the new agent with the tag
        new_agent_tag = models.AgentTag(
            agent_id=new_agent.id,
            tag_id=tag.id
        )

        # Add the new AgentTag to the session
        db.add(new_agent_tag)
        db.flush()
    db.commit()
    return "Added agent and tags successfully"


def save_saved_data(user_id, content, tags):
    # Create a new SavedData object
    new_saved_data = models.SavedData(
        user_id=user_id,
        content=content
    )

    # Add the new SavedData object to the session
    db.add(new_saved_data)
    db.flush()

    # For each tag in the list of tags
    for tag_name in tags:
        # Query the Tag table to see if this tag already exists
        tag = db.query(models.Tag).filter(models.Tag.tag == tag_name).first()

        # If the tag doesn't exist, create a new one
        if tag is None:
            tag = models.Tag(tag=tag_name)
            db.add(tag)
            db.flush()

        # Create a new DataTag linking the new saved data with the tag
        new_data_tag = models.DataTag(
            data_id=new_saved_data.id,
            tag_id=tag.id
        )

        # Add the new DataTag to the session
        db.add(new_data_tag)
        db.flush()
    db.commit()
    return "Added saved data and tags successfully"

### Retrieve stuff
def get_message_history(user_id, period=None, start_date=None, end_date=None):
    """Retrieves the message history for a specific user."""
    query = db.query(models.Message_history).filter(models.Message_history.user_id == user_id)

    if period:
        if period == 'day':
            start_date = datetime.now() - timedelta(days=1)
        elif period == 'week':
            start_date = datetime.now() - timedelta(weeks=1)
        elif period == 'month':
            start_date = datetime.now() - timedelta(weeks=4)

    if start_date and end_date:
        query = query.filter(models.Message_history.timestamp >= start_date,
                             models.Message_history.timestamp <= end_date)
    elif start_date:
        query = query.filter(models.Message_history.timestamp >= start_date)

    return [x.to_dict() for x in query.all()]

def get_agent(user_id=None, agent_name=None):
    """Retrieves the agent based on provided parameters."""

    query = db.query(models.Agent)

    if agent_name:
        query = query.filter(models.Agent.agent_name == agent_name)
    elif user_id:
        query = query.filter(models.Agent.user_id == user_id)

    return [x.to_dict() for x in query.all()]
def get_saved_data(user_id=None, tags=None, period=None, start_date=None, end_date=None):
    """Retrieves the saved data based on provided parameters."""

    query = db.query(models.SavedData)

    if user_id:
        query = query.filter(models.SavedData.user_id == user_id)
    elif tags:
        # Assuming `tags` is a list of tags.
        query = query.join(models.SavedData.tags).filter(models.Tag.tag.in_(tags))

    if period:
        if period == 'day':
            start_date = datetime.now() - timedelta(days=1)
        elif period == 'week':
            start_date = datetime.now() - timedelta(weeks=1)
        elif period == 'month':
            start_date = datetime.now() - timedelta(weeks=4)

    if start_date and end_date:
        query = query.filter(models.SavedData.timestamp >= start_date,
                             models.SavedData.timestamp <= end_date)
    elif start_date:
        query = query.filter(models.SavedData.timestamp >= start_date)

    return [x.to_dict() for x in query.all()]

db.close()
