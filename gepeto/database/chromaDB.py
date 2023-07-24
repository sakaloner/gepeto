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

client = chromadb.Client(
    Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory="./chroma/"
    )
)
class ChromaDB:
    def __init__(self):
        self.priv_col = client.get_or_create_collection("private")
        self.public_col = client.get_or_create_collection("public")
