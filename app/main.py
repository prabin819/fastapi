# fastapi dev main.py --reload
# uvicorn main:app --reload
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine) 
# we no longer need this since we are using alembic
# this was the statement that was responsible for creating tables (using sqlalchemy)

app = FastAPI()

origins = ["https://www.google.com"]    #list of all the domains that will talk to our api

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# my_posts = [{"id": 1, "title": "title of post 1", "content": "this is content of post 1"},{"id": 2, "title": "title of post 2", "content": "this is content of post 2"}]

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Welcome to python fast API with postgres!!!!!!"}