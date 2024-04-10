from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import register_user, like_user, login_user, dislike_user, get_unseen_users, get_modules, get_questions, get_all_chats, create_text, get_chat
from models import reg_user_model, login_user_model, like_model, dislike_model, chat_model, chat_text_model



app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://localhost:4040",
    "https://positive-clearly-tiger.ngrok-free.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/register")
def register(user: reg_user_model):
    register_user(user)
    return {"message": "Student registered successfully!"}

@app.post("/login")
def login(user: login_user_model):
    return login_user(user)

@app.post("/like")
def like(like: like_model):
    return like_user(like)

@app.post("/dislike")
def dislike(dislike: dislike_model):
    dislike_user(dislike)
    return {"message": "Student disliked successfully!"}

@app.get("/unseen/{id}")
def unseen(id: int):
    return {"unseen": get_unseen_users(id)}

@app.get("/courses/{course}")
def modules(course: str):
    return get_modules(course)

@app.get("/questions/{course}/{module}/{subheading}")
def questions(course: str, module: str, subheading: str):
    return get_questions(course, module, subheading)

@app.post("/text")
def text(chat_text: chat_text_model):
    return create_text(chat_text)

@app.get("/chat/{id1}/{id2}")
def chat(id1: int, id2: int):
    return get_chat(id1, id2)

@app.get("/chats")
def chats(id: int):
    return get_all_chats(id)