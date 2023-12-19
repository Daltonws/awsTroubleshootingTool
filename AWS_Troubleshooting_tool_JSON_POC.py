from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

def get_chat_response(platform, services, error_code, runtime, error_description, api_key):
    """
    Sends a request to the OpenAI ChatGPT model.
    Constructs a message asking for a description of the error and recommendations.

    :param platform: The platform where the error occurred
    :param services: List of services encountering the error
    :param error_code: The specific error code encountered
    :param runtime: The runtime environment where the error occurred
    :param error_description: A brief description of the issue
    :param api_key: OpenAI API key for authentication
    :return: The response message from ChatGPT
    """
    url = "https://api.openai.com/v1/chat/completions"

    services_str = ", ".join(services)
    runtime_info = f"Runtime: {runtime}\n" if runtime else ""
    prompt_message = (
        f"I encountered a {error_code} error on the {platform} platform with services {services_str}.\n"
        f"{runtime_info}"
        f"Error Description: {error_description}\n"
        f"Can you provide a detailed description of this error and recommend actions to resolve it?"
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
    :return: A tuple containing the error description and a list of recommendations
    """
    parts = re.split(r'\d+\.', response)
    description = parts[0].strip()
    recommendations = [part.strip() for part in parts[1:]]

    return description, recommendations

@app.route('/troubleshoot/json', methods=['POST'])
def troubleshoot():
    """
    Flask route to handle POST requests for AWS error troubleshooting.
    It receives error details and interacts with ChatGPT to return a JSON response.
    """
    data = request.json
    platform = data.get('platform')
    services = data.get('service', [])
    error_code = data.get('error_code', '')
    runtime = data.get('runtime', '')  # Extracting the runtime information
    error_description = data.get('error_description', '')
    api_key = "your_api_key"  # Replace with your actual API key

    chat_response = get_chat_response(platform, services, error_code, runtime, error_description, api_key)
    description, recommendations = parse_response(chat_response)

    # Return the response as JSON
    return jsonify({
        "error_description": description,
        "solution_recommendations": recommendations
    })

if __name__ == "__main__":
    app.run(debug=True)
