from flask import Flask, request, jsonify
import requests
from markupsafe import Markup
import re

# Initialize the Flask application
app = Flask(__name__)

def get_chat_response(aws_service, error_code, description, api_key):
    """
    Function to send a request to the OpenAI ChatGPT model.
    It constructs a message asking for a description of an AWS service error
    and recommendations to resolve it.

    :param aws_service: The AWS service encountering the error
    :param error_code: The specific error code encountered
    :param description: A brief description of the issue
    :param api_key: OpenAI API key for authentication
    :return: The response message from ChatGPT
    """
    url = "https://api.openai.com/v1/chat/completions"

    # Constructing the message to send to ChatGPT
    prompt_message = (
        f"I encountered an error with the AWS service {aws_service}.\n"
        f"Error Code: {error_code}\n"
        f"Description: {description}\n"
        f"Can you provide a description of this error and recommend actions to resolve it?"
    )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "temperature": 0.3,
        "messages": [{"role": "user", "content": prompt_message}]
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()['choices'][0]['message']['content'] if response.status_code == 200 else f"Error: {response.text}"

def parse_response(response):
    """
    Parses the ChatGPT response to separate the error description and the list of recommendations.
    
    :param response: The response string from ChatGPT
    :return: A tuple containing the error description and the HTML formatted recommendations
    """
    # Split the response into parts at each numbered item
    parts = re.split(r'\d+\.', response)
    description = parts[0].strip()

    # Reformat the recommendations as an HTML ordered list
    recommendations = '<ol>' + ''.join([f'<li>{part.strip()}</li>' for part in parts[1:]]) + '</ol>'

    return description, recommendations

@app.route('/troubleshoot', methods=['POST'])
def troubleshoot():
    """
    Flask route to handle POST requests for AWS error troubleshooting.
    It receives the error details, interacts with ChatGPT, and returns an HTML formatted response.
    """
    data = request.json
    aws_service = data.get('aws_service')
    error_code = data.get('error_code')
    description = data.get('description')
    api_key = "your_api_key"  # Replace with your actual API key

    chat_response = get_chat_response(aws_service, error_code, description, api_key)
    description, recommendations = parse_response(chat_response)

    # Format and return the response as HTML
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
