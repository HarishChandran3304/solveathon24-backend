from fastapi import FastAPI
from db import register_user, like_user, dislike_user, get_unseen_users
from models import reg_user_model, like_model, dislike_model


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/register")
def register(user: reg_user_model):
    register_user(user)
    return {"message": "Student registered successfully!"}

@app.post("/like")
def like(like: like_model):
    return like_user(like)

@app.post("/dislike")
def dislike(dislike: dislike_model):
    dislike_user(dislike)
    return {"message": "Student disliked successfully!"}

@app.get("/unseen/{id}")
def get_unseen(id: int):
    return {"unseen": get_unseen_users(id)}