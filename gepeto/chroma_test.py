#!/usr/bin/env python3
import chromadb
from chromadb.utils import embedding_functions
from chromadb.config import Settings
from dotenv import load_dotenv
import os
import openai
from database import crud
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

## embeddings
default_ef = embedding_functions.DefaultEmbeddingFunction()
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                model_name="text-embedding-ada-002"
            )

chroma_client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="./database/chroma/"
))

res = crud.get_message_history(0, 'week')

messages = [x['message'] for x in res]
ids = [str(x['id']) for x in res]
directions = [{'role':x['direction']} for x in res]

#collection = chroma_client.create_collection(name="message3", embedding_function=default_ef)



col = chroma_client.get_collection('message3')
col.add(
    documents=messages,
    metadatas=directions,
    ids=ids,
)
results = col.query(
    query_texts=["who the fuck are you"],
    where={'role':'User'},
    n_results=10
)

print(results)
