#!/usr/bin/env python3
from database.chromaDB import ChromaDB
from database import crud
from time import time

print('hello world')
chroma = ChromaDB()
print('passed')
res = chroma.public_col.peek()

results = col.query(
    query_texts=["who the fuck are you"],
    where={'role':'User'},
    n_results=10
)
