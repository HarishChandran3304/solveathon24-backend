import requests
import json
import os
from dotenv import load_dotenv


load_dotenv()


def generate_modules(course):
    text_prompt = f"""for an online quiz-based course on the programming language {course}, formulate 8 modules (structures that will serve as chapters/units) that go from basics to project implementation in that language, with 5 subheadings under each module without any conversational text, in json format.
the response should be in format
{{
    modules: {{
        name: string;
        subheadings: string[];
    }}[]
 }}"""
    
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={os.getenv("GEMINI_API_KEY")}'
    headers = {'Content-Type': 'application/json'}
    data = {"contents":[{"parts":[{"text":str(text_prompt)}]}]}

    response = requests.post(url, headers=headers, data=json.dumps(data))

    # To print the response
    return stringToJSON(parseResponse(response.json()["candidates"][0]["content"]["parts"][0]["text"]))

def generate_questions(course, module, subheading):
    text_prompt = f'''for a course on the programming language {course}, under the heading {module}, for the subheading {subheading}, generate 10 multiple-choice questions with 3 choices for each question in a json format, with the information in the following format:
question
choice 1
choice 2
choice 3
correct answer in the format of an integer that marks which of the answers it is

the response should be in format
{{
    questions: {{
            question: string;
            choice1: string;
            choice2: string;
            choice3: string;
            correctAnswer: number;
    }}[];
}}'''
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={os.getenv("GEMINI_API_KEY")}'
    headers = {'Content-Type': 'application/json'}
    data = {"contents":[{"parts":[{"text":str(text_prompt)}]}]}

    response = requests.post(url, headers=headers, data=json.dumps(data))

    # To print the response
    return stringToJSON(parseResponse(response.json()["candidates"][0]["content"]["parts"][0]["text"]))


def parseResponse(response: str):
    '''
    Parse the response from the Gemini API
    Get the text in between the triple backticks
    '''
    print(response)
    if "```" in response:
        response = "a" + response
        return response.split("```")[1].replace("json\n", "")
    else:
        return response

def stringToJSON(string: str) -> dict:
    '''
    Convert a string to a JSON object
    '''
    return json.loads(string)


if __name__ == "__main__":
    print(generate_questions("JavaScript", "Introduction to JavaScript", "What is JavaScript?"))