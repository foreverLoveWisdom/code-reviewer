from flask import Flask, render_template
import openai
import markdown2
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Prompt message for code review
CODE_REVIEW_PROMPT = """
* Act as the most meticulous Pull Request reviewer in history, evaluating the <following code>, detecting its language/framework, and checking it against the following criteria:
  * Provide practical, actionable suggestions/improvements.
  * Follow common conventions, SOLID principles, readability, maintainability, security best practices.
  * Ensure clear and concise naming, consistent formatting, and distinguishable identifiers.

  * Use ‼️ emoji for critical suggestions, sorted by priority (higher priority on top).
"""

def request_code_review(file_content, model):
    """Request code review using OpenAI GPT-3 model."""
    messages = [
        {"role": "system", "content": CODE_REVIEW_PROMPT},
        {"role": "user", "content": f"Code review the following file: {file_content}"},
    ]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
    )
    return response.choices[0]["message"]["content"]

def start_code_review():
    """Initiate code review process."""
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
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
