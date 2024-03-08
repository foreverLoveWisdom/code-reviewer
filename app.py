import os
import markdown2
from dotenv import load_dotenv
from flask import Flask, render_template
from anthropic import Anthropic
import pretty_errors

app = Flask(__name__)

client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
)

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
    response = client.messages.create(
        max_tokens=4096,
        temperature=0.0,
        # system=CODE_REVIEW_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Code review the following file: {file_content}",
            }
        ],
        model=model,
    )
    return response.content[0].text


def start_code_review():
    """Initiate code review process."""
    load_dotenv()
    model = os.getenv("CLAUDE_MODEL") or "claude-3-sonnet-20240229"
    filename = os.getenv("FILENAME") or "test.txt"
    with open(filename, "r") as file:
        file_content = file.read()
    return request_code_review(file_content, model)


@app.route("/")
def render_code_review_result():
    """Render code review result."""
    content = start_code_review()
    result = markdown2.markdown(content)
    return render_template("code_review.html", result=result)
