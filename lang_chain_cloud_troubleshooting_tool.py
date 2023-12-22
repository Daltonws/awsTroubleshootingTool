from flask import Flask, request, jsonify
from markupsafe import Markup
import os
import re
from langchain.chains import GPT

# Initialize the Flask application and Langchain GPT component
app = Flask(__name__)
gpt = GPT(api_key=os.environ.get('OPENAI_API_KEY'))

def get_chat_response_with_langchain(aws_service, error_code, description):
    """
    Function to interact with the Langchain GPT component.
    It constructs a message asking for a description of an AWS service error
    and recommendations to resolve it.

    :param aws_service: The AWS service encountering the error
    :param error_code: The specific error code encountered
    :param description: A brief description of the issue
    :return: The response message from GPT
    """
    prompt_message = (
        f"I encountered an error with the AWS service {aws_service}.\n"
        f"Error Code: {error_code}\n"
        f"Description: {description}\n"
        f"Can you provide a description of this error and recommend actions to resolve it?"
    )
    response = gpt.complete(prompt_message)
    return response

def parse_response(response):
    """
    Parses the GPT response to separate the error description and the list of recommendations.
    
    :param response: The response string from GPT
    :return: A tuple containing the error description and the HTML formatted recommendations
    """
    parts = re.split(r'\d+\.', response)
    description = parts[0].strip()
    recommendations = '<ol>' + ''.join([f'<li>{part.strip()}</li>' for part in parts[1:]]) + '</ol>'
    return description, recommendations

@app.route('/troubleshoot', methods=['POST'])
def troubleshoot():
    """
    Flask route to handle POST requests for AWS error troubleshooting.
    It receives the error details, interacts with GPT through Langchain, and returns an HTML formatted response.
    """
    data = request.json
    aws_service = data.get('aws_service')
    error_code = data.get('error_code')
    description = data.get('description')

    if not all([aws_service, error_code, description]):
        return "Missing data", 400

    chat_response = get_chat_response_with_langchain(aws_service, error_code, description)
    description, recommendations = parse_response(chat_response)

    html_response = Markup(f"""
    <html>
        <head>
            <title>Troubleshoot Response</title>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .response, .recommendations {{ padding: 20px; background-color: #f0f0f0; border: 1px solid #ddd; }}
                .recommendations {{ margin-top: 20px; }}
            </style>
        </head>
        <body>
            <h2>Error Description</h2>
            <div class="response">{description}</div>
            <h2>Solution Recommendations</h2>
            <div class="recommendations">{recommendations}</div>
        </body>
    </html>
    """)
    return html_response

if __name__ == "__main__":
    app.run(debug=True)
