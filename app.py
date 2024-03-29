from flask import Flask, render_template
from openai import OpenAI
import langchain
from langchain .text_splitter import RecursiveCharacterTextSplitter

import markdown2
from dotenv import load_dotenv
import os

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# Prompt message for code review
CODE_REVIEW_PROMPT = """
As a meticulous Pull Request reviewer, thoroughly evaluate the <following code> for language/framework, adhering to the following criteria:
    * Use the ‼️ emoji to highlight critical suggestions, sorted by priority (with higher priority suggestions listed first).
    * Focus on maintainability, readability, simplicity, adaptability to new business requirements change
    * Naming:
        * Understandabiliy: Should describe the concept it designs
        * Conciseness: Should use only the words necessary to describe the concept it represents
        * Consistency: Should be used and formatted uniformly
        * Distinguishability: Should be visually and phonetically distinct from other names used within its scope
    * Provide before and after examples if possible
    * Explain your thought process step by step calmly
"""

def request_code_review(file_content, model):
    """Request code review using OpenAI GPT-3 model."""
    messages = [
        {"role": "system", "content": CODE_REVIEW_PROMPT},
        {"role": "user", "content": f"Code review the following file: {file_content}"},
    ]
    response = client.chat.completions.create(model=model,
    messages=messages, temperature=0.3)
    return response.choices[0].message.content

def start_code_review():
    """Initiate code review process."""
    load_dotenv()
    model = os.getenv("OPENAI_MODEL") or "gpt-3.5-turbo"  # Set default model
    filename = os.getenv("FILENAME") or "test.txt"  # Set default filename
    with open(filename, "r") as file:
        file_content = file.read()
    return request_code_review(file_content, model)

@app.route("/")
def render_code_review_result():
    """Render code review result."""
    content = start_code_review()
    result = markdown2.markdown(content)
    return render_template("code_review.html", result=result)
