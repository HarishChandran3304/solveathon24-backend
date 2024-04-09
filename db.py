from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from models import reg_user_model, fetch_user_model, like_model, dislike_model, match_model
import os


load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"), server_api=ServerApi('1'))
db = client["v-konnekt"]
users = db["users"]
likes = db["likes"]
matches = db["matches"]


def register_user(reg_user: reg_user_model):
    reg_no = reg_user.reg_no
    passwd = reg_user.passwd

    user = {
        "id": users.count_documents({}) + 1,
        "reg_no": reg_no,
        "passwd": passwd,
        "name": "",
        "tagline": "",
        "department": "",
        "batch": "",
        "last_seen": "",
        "github": "",
        "linkedin": "",
        "twitter": "",
        "skills": [],
        "looking_for": []
    }
    
    users.insert_one(user)

def like_user(like: like_model):
    '''
    Check if from_id has already been liked by to_id
    If yes, remove the like and add a match
    If no, add the like
    '''
    from_id = like.from_id
    to_id = like.to_id

    if likes.count_documents({"from_id": to_id, "to_id": from_id}) > 0:
        likes.delete_one({"from_id": to_id, "to_id": from_id})
        match_users({"id1": from_id, "id2": to_id})
        return {"message": "Matched!"}
    else:
        likes.insert_one({"from_id": from_id, "to_id": to_id})
        return {"message": "Liked!"}

def dislike_user(dislike: dislike_model):
    '''
    If the to_id has liked from_id, remove the like
    '''
    from_id = dislike.from_id
    to_id = dislike.to_id

    if likes.count_documents({"from_id": to_id, "to_id": from_id}) > 0:
        likes.delete_one({"from_id": to_id, "to_id": from_id})

def match_users(match: match_model):
    '''
    Add a match between the two users
    '''
    id1 = match["id1"]
    id2 = match["id2"]

    matches.insert_one({"id1": id1, "id2": id2})