from fastapi import FastAPI
from db import register_student
from models import student_reg


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/register")
def register(student: student_reg):
    register_student(student)
    return {"message": "Student registered successfully!"}