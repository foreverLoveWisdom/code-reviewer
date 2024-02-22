- 🐍 This Python Flask application leverages OpenAI's GPT model to conduct automated code reviews. It allows users to input code for review and receive actionable feedback based on predefined criteria. The application is designed to assist developers/tech leads/managers in improving their code quality and adhering to best practices.
- 📝 This is just a guide to get you started. You can customize the `prompt` to suit your needs.

* To run the application:

1. Install dependencies: `pip install flask openai markdown2 python-dotenv`
2. Set up your OpenAI API key by creating a `.env` file in the root directory and adding your API key: `OPENAI_API_KEY=your_api_key_here`
3. Run the Flask app: `flask run`
4. You must extract the git diff and write it to a file. Currently, this file name is hardcoded to `test.txt`. There is a sample file in the root

- 🚀 How to use:

1. Navigate to the home page.
2. Input the code you want to review.
3. Submit the code for review.
4. Receive detailed feedback on SOLID principles, readability, maintainability, security, and best practices.
5. Use the actionable suggestions to improve your code.

- ℹ️ Note:
  - This application is intended for educational and training purposes. It provides insights and suggestions but does not replace human code review.
  - This is a paid API. To use this application, you must sign up for an API key at [OPENAI](https://platform.openai.com/overview).

* For more information on how the code review process works, refer to the `code_review.html` template in the `templates` directory.

* 💡 Suggestions for improvements:

  - Update the `prompt` to include more specific criteria for code review that suit your team's needs.
  - Allow users to upload files for review or automatically pull code from a repository, extract the diff, and submit it for review.
  - Add a feature to compare code before and after changes.
  - Add interactive features to the code review process.
  - Remember, this is just a guide to get you started. Customize the `prompt` to suit your needs.

* Enjoy improving your code with AI-powered reviews!
