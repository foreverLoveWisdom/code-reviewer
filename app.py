from flask import Flask, render_template
import openai
import markdown2
from dotenv import load_dotenv
import os
import threading

app = Flask(__name__)

PROMPT = """
Act as a master of code review and review the following code
"""


def make_code_review_request(filecontent, model):
    messages = [
        {"role": "system", "content": PROMPT},
        {"role": "user", "content": f"Code review the following file: {filecontent}"},
    ]

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
    )

    return response.choices[0]["message"]["content"]


def start_code_review():
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    model = "gpt-3.5-turbo"  # Set your preferred model here
    filename = "test.txt"  # Hardcoded filename

    with open(filename, "r") as file:
        filecontent = file.read()
    return make_code_review_request(filecontent, model)


@app.route("/")
def render_code_review_result():
    content = start_code_review()
    result = markdown2.markdown(content)
    return render_template("code_review.html", result=result)
