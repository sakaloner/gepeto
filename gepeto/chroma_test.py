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
collection = chroma_client.create_collection(name="new_col", embedding_function=default_ef)

collection.add(
    documents=["this is a message for all the people on earth", "i am feeling kinda sad right now uwu"],
    metadatas=[{"source": "my_source"}, {"source": "my_source"}],
    ids=["id1", "id2"]
)
results = collection.query(
    query_texts=["lets just work together for a better future"],
    n_results=1
)
print(results)
