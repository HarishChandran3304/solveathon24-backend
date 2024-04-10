from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from models import reg_user_model, login_user_model, fetch_user_model, like_model, dislike_model, match_model, chat_model, chat_text_model
from ai import generate_modules, generate_questions
import os
from datetime import datetime


load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"), server_api=ServerApi('1'))
db = client["v-konnekt"]
users = db["users"]
likes = db["likes"]
matches = db["matches"]
courses = db["courses"]
questions = db["questions"]
chats = db["chats"]


def register_user(reg_user: reg_user_model):
    reg_no = reg_user.reg_no
    passwd = reg_user.passwd
    name = reg_user.name
    tagline = reg_user.tagline
    description = reg_user.description
    skills = reg_user.skills
    looking_for = reg_user.looking_for
    types = reg_user.types


    user = {
        "id": users.count_documents({}) + 1,
        "reg_no": reg_no,
        "passwd": passwd,
        "name": name,
        "tagline": tagline,
        "description": description,
        "github": "https://github.com/HarishChandran3304",
        "linkedin": "https://www.linkedin.com/in/theditor/",
        "twitter": "https://twitter.com/nottheditor",
        "skills": skills,
        "looking_for": looking_for,
        "types": types
    }
    
    users.insert_one(user)

def login_user(login_user: login_user_model):
    reg_no = login_user.reg_no
    passwd = login_user.passwd

    if users.count_documents({"reg_no": reg_no, "passwd": passwd}) > 0:
        return {"username": reg_no, "user": users.find_one({"reg_no": reg_no, "passwd": passwd}, {"_id": 0})["name"]}

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

def get_unseen_users(id: int) -> set:
    '''
    Get users that the user with id has not seen
    Unseen users are all users minus the users in liked and matches
    '''
    #set of all users
    all_users = set([user["id"] for user in users.find()]) - {id}

    #set of users in liked by id
    liked = set([like["to_id"] for like in likes.find({"from_id": id})])

    #set of users in matched with id
    matched = set([match["id1"] for match in matches.find({"id2": id})])

    #set of unseen users
    unseen = all_users - liked - matched

    res = []
    for id in unseen:
        temp = {}
        temp["imageUrl"] = "https://api.dicebear.com/8.x/bottts/png"
        temp["name"] = users.find_one({"id": id}, {"_id": 0, "name": 1})["name"]
        temp["tagline"] = users.find_one({"id": id}, {"_id": 0, "tagline": 1})["tagline"]
        temp["skills"] = users.find_one({"id": id}, {"_id": 0, "skills": 1})["skills"]
        temp["lookingfor"] = users.find_one({"id": id}, {"_id": 0, "looking_for": 1})["looking_for"]
        temp["types"] = users.find_one({"id": id}, {"_id": 0, "types": 1})["types"]
        temp["id"] = str(id)
        temp["description"] = "This is a description of the user." 

        res.append(temp)
    
    return res

def get_modules(course: str) -> dict:
    '''
    Get the modules for the course
    If it exists in the modules collection then return it
    Else generate the modules insert into the database and return it
    '''
    if courses.count_documents({"course": course}) > 0:
        return courses.find_one({"course": course}, {"_id": 0})
    else:
        modules = generate_modules(course)
        courses.insert_one({"course": course} | dict(modules))
        return courses.find_one({"course": course}, {"_id": 0})

def get_questions(course: str, module: str, subheading: str) -> dict:
    '''
    Get the questions for the course
    If it exists in the questions collection then return it
    Else generate the questions insert into the database and return it
    '''
    if questions.count_documents({"course": course, "module": module, "subheading": subheading}) > 0:
        return questions.find_one({"course": course, "module": module, "subheading": subheading}, {"_id": 0})
    else:
        qs = generate_questions(course, module, subheading)
        questions.insert_one({"course": course, "module": module, "subheading": subheading} | dict(qs))
        return questions.find_one({"course": course, "module": module, "subheading": subheading}, {"_id": 0})
    
def create_chat(chat: chat_model):
    '''
    Create a chat between the two users
    '''
    chats.insert_one(chat)

def create_text(chat_text: chat_text_model):
    '''
    Add a text to the chat
    '''
    from_id = chat_text.from_id
    to_id = chat_text.to_id
    message = chat_text.message
    timestamp = datetime.now().isoformat()

    chats.update_one({"id1": from_id, "id2": to_id}, {"$push": {"messages": {"from_id": from_id, "message": message, "timestamp": timestamp}}})

    return {"message": "Text sent successfully!"}

def get_chat(id1: int, id2: int) -> list:
    '''
    Get the chat between the two users
    '''
    chat = chats.find_one({"id1": id1, "id2": id2}, {"_id": 0})

    res = {"messages": []}
    for message in chat["messages"]:
        temp = {}
        temp["author"] = "self" if message["from_id"] == id1 else str(id2)
        temp["message"] = message["message"]

        res["messages"].append(temp)
    
    return res


def get_user_name(id: int) -> str:
    '''
    Get the name of the user with id
    '''
    return users.find_one({"id": id}, {"_id": 0, "name": 1})["name"]

def get_all_chats(id: int) -> list:
    '''
    Get all the chats for the user
    Get all chats where id1 is id
    '''
    all_chats = []
    for chat in chats.find({"id1": id}, {"_id": 0}):
        temp = {
            "userid": str(chat["id2"]),
            "user": get_user_name(chat["id2"]),
            "lastMessage": chat["messages"][-1]["message"],
            "status": 0,
            "image": "https://api.dicebear.com/8.x/bottts/png",
            "time": chat["messages"][-1]["timestamp"]
        }
        all_chats.append(temp)
    
    return all_chats



if __name__ == "__main__":
    get_questions("JavaScript", "Introduction to JavaScript", "What is JavaScript?")


'''
# TODO
Chat
- list of msgs btw 2 ids
- list of matches, last msg, last msg time
- send msg
'''
