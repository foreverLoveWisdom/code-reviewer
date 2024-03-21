import os
import pprint

import markdown2
import pretty_errors
from anthropic import Anthropic
from dotenv import load_dotenv
from flask import Flask, render_template

app = Flask(__name__)


# Prompt message for code review
CODE_REVIEW_PROMPT = """
As a holistic Pull Request reviewer, thoroughly evaluate the <following code>, adhering to the following criteria:
    * First try to guess the programming language/framework and the high level purpose of the code
    * Then, validate its against the best practices/conventions and standards of the language/framework
    * Focus on maintainability, readability, simplicity, adaptability
    * Naming:
        * Understandabiliy: Should describe the concept it designs
        * Conciseness: Should use only the words necessary to describe the concept it represents
        * Consistency: Should be used and formatted uniformly
        * Distinguishability: Should be visually and phonetically distinct from other names used within its scope
    * Before answering the question, please think about it step-by-step within <thinking></thinking> tags.
    * Then, provide your final answer within <answer></answer> tags.
    * Prioritize your suggestions from most important to least important, top to bottom.
    * Rank the whole this whole PR from 1 to 5, 1 being the worst and 5 based on the given criteria.
    * Your suggestions should be actionable, specific, with clear examples, and explicitly state the trade-offs for each of them, and then pick the one that is align with the previous goals
    * Mention which step needs human intervention.
    * Finally, keep these concise and to the point, avoiding unnecessary verbosity for non-native English speakers.
"""


def request_code_review(file_content, model):
    client = Anthropic(
        api_key=os.getenv("ANTHROPIC_API_KEY"),
    )
    response = client.messages.create(
        max_tokens=4096,
        temperature=0.0,
        system=CODE_REVIEW_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Code review the following file: {file_content}",
            }
        ],
        model=model,
    )
    pprint.pprint(response)
    return response.content[0].text


def start_code_review():
    """Initiate code review process."""
    load_dotenv()
    # Legacy model is more expensive
    # Currently the Haiku model is the fastest and cheapest, but not released
    # yet
    model = os.getenv("CLAUDE_MODEL") or "claude-3-haiku-20240307"
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
