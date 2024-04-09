from pydantic import BaseModel


class reg_user_model(BaseModel):
    reg_no: str
    passwd: str

class fetch_user_model(BaseModel):
    id: int
    reg_no: str
    passwd: str
    name: str
    tagline: str
    department: str
    batch: int
    last_seen: str
    github: str
    linkedin: str
    twitter: str
    skills: list[str]
    looking_for: list[str]

class like_model(BaseModel):
    from_id: int
    to_id: int

class dislike_model(BaseModel):
    from_id: int
    to_id: int

class match_model(BaseModel):
    id1: int
    id2: int