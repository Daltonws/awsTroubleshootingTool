# AWS Error Troubleshooting Flask Application

This Flask application serves as an interface between the user and the OpenAI ChatGPT API. It allows users to submit details about an AWS service error and receive a structured response with a description of the error and recommended actions to resolve it.

## Features

- Sends queries to OpenAI's ChatGPT API.
- Parses ChatGPT's response to separate error descriptions and recommendations.
- Formats the response in an HTML structure for better readability.
- Includes a React front-end for user interaction with the application.
- Provides visual feedback and acknowledgement on form submission status in the UI.

## Setup and Installation

1. **Install Required Packages**: Run `pip install flask requests markupsafe` to install the necessary Python packages for the Flask server. For the React front-end, ensure Node.js and npm are installed, then run `npm install` in the React project directory.
2. **API Key**: Obtain an OpenAI API key and replace `your_api_key` in the code with your actual API key.
3. **Running the Flask Application**: Execute the Flask script to start the Flask server. By default, it runs on `http://127.0.0.1:5000/`.
4. **Running the React Application**: Navigate to the React project directory and run `npm start` to start the React development server. The front-end interface will be available at `http://localhost:3000/`.

## Usage

### Backend

Send a POST request to `http://127.0.0.1:5000/troubleshoot` with a JSON payload containing `platform`, `service`, `error_code`, `runtime`, and `error_description` fields.

Example JSON payload:
```json
{
    "platform": "AWS",
    "service": ["Lambda", "API Gateway"],
    "error_code": "502",
    "runtime": "",
    "error_description": "InvalidRuntimeException"
}
