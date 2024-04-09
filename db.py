from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from models import student_reg
import os


load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"), server_api=ServerApi('1'))
db = client["v-konnekt"]
students = db["students"]
likes = db["likes"]


def register_student(student_reg: student_reg):
    # reg_no = student_reg.reg_no
    # passwd = student_reg.passwd

    student = {
        "id": students.count_documents({}) + 1,
        "reg_no": "reg_no",
        "passwd": "passwd",
        "name": "",
        "department": "",
        "last_seen": ""
    }
    
    students.insert_one(student)


if __name__ == "__main__":
    print("Running db.py as main file")
    print(register_student("22BRS1149", "password"))
    print("Done!")