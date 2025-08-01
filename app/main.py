# fastapi dev main.py --reload
# uvicorn main:app --reload
from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session
from typing import cast, List
from .routers import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# database connection (psycopg)
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='krishna', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('database connection was successful')
        break
    except Exception as error:
        print('Connection to database failed.')
        print('Error: ', error)
        time.sleep(3)


my_posts = [{"id": 1, "title": "title of post 1", "content": "this is content of post 1"},{"id": 2, "title": "title of post 2", "content": "this is content of post 2"}]

app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "Welcome to python fast API with postgres!!!!!!"}