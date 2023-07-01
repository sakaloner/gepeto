#!/usr/bin/env python3
import sqlalchemy
from sqlalchemy import Boolean, Enum, Column, func, ForeignKey, Integer, String, DateTime, Table
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.main import Base
from sqlalchemy.ext.declarative import DeclarativeMeta
import json

class Message_history(Base):
    __tablename__ = 'message_history'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    message = Column(String, nullable=False)
    timestamp = Column(DateTime, default=func.now())
    direction = Column(Enum('Assistant', 'User', name='direction'), nullable=False)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=True)
    telegram_id = Column(String, nullable=True)
    whatsapp_id = Column(String, nullable=True)
    premium = Column(Boolean)
    messages = relationship('Message_history', backref='user')

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
class DataTag(Base):
    __tablename__ = 'data_tag'

    id = Column(Integer, primary_key=True)
    data_id = Column(Integer, ForeignKey('saved_data.id'), nullable=False)
    tag_id = Column(Integer, ForeignKey('tag.id'), nullable=False)

class AgentTag(Base):
    __tablename__ = 'agent_tag'

    id = Column(Integer, primary_key=True)
    agent_id = Column(Integer, ForeignKey('agent.id'), nullable=False)
    tag_id = Column(Integer, ForeignKey('tag.id'), nullable=False)

class SavedData(Base):
    __tablename__ = 'saved_data'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, default=func.now())
    tags = relationship('Tag', secondary='data_tag', back_populates='saved_data')  # Change here

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
class Tag(Base):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)
    tag = Column(String, nullable=False, unique=True)
    saved_data = relationship('SavedData', secondary='data_tag', back_populates='tags')  # Change here
    agents = relationship('Agent', secondary='agent_tag', back_populates='tags')  # Added this line

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
class Agent(Base):
    __tablename__ = 'agent'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    agent_prompt = Column(String, nullable=False)
    agent_name = Column(String, nullable=False)
    timestamp = Column(DateTime, default=func.now())
    tags = relationship('Tag', secondary='agent_tag', back_populates='agents')  # Change here

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
