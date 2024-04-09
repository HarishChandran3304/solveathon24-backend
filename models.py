from pydantic import BaseModel


class student_reg(BaseModel):
    reg_no: str
    passwd: str

class student_fetch(BaseModel):
    id: str
    reg_no: str
    passwd: str
    name: str
    department: str
    last_seen: str
    skills: list[str]
    looking_for: list[str]