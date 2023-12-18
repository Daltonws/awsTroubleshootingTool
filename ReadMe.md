# AWS Error Troubleshooting Flask Application

This Flask application serves as an interface between the user and the OpenAI ChatGPT API. It allows users to submit details about an AWS service error and receive a structured response with a description of the error and recommended actions to resolve it.

## Features

- Sends queries to OpenAI's ChatGPT API.
- Parses ChatGPT's response to separate error descriptions and recommendations.
- Formats the response in an HTML structure for better readability.

## Setup and Installation

1. **Install Required Packages**: Run `pip install flask requests markupsafe` to install the necessary Python packages.
2. **API Key**: Obtain an OpenAI API key and replace `your_api_key` in the code with your actual API key.
3. **Running the Application**: Execute the script to start the Flask server. By default, it runs on `http://127.0.0.1:5000/`.

## Usage

Send a POST request to `http://127.0.0.1:5000/troubleshoot` with a JSON payload containing `aws_service`, `error_code`, and `description` fields.

Example JSON payload:
```json
{
    "aws_service": "EC2",
    "error_code": "SomeError",
    "description": "Description of the error"
}
