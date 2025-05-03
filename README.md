# Weather Agent

This project is a simple Weather Agent that provides weather information for a given city. It uses OpenWeatherMap API for weather data and AWS Bedrock for AI-based query processing.

## Features
- Fetches weather information for a given city.
- Supports natural language queries.
- Simple web-based UI.

## Prerequisites
- Python 3.13 or higher
- An OpenWeatherMap API key
- AWS credentials with access to Bedrock

## Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd weather-agent
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add the following environment variables:
   ```env
   WEATHER_API_KEY=<your_openweathermap_api_key>
   AWS_REGION=<your_aws_region>
   AWS_ACCESS_KEY_ID=<your_aws_access_key_id>
   AWS_SECRET_ACCESS_KEY=<your_aws_secret_access_key>
   AWS_SESSION_TOKEN=<your_aws_session_token>
   ```

## Running the Application
1. Start the server:
   ```bash
   python3 weather_ui.py
   ```

2. Open your browser and navigate to `http://localhost:8000`.

## File Structure
- `weather_model.py`: Contains the logic for interacting with the AWS model and the weather API.
- `weather_ui.py`: Handles the UI and HTTP server logic.
- `requirements.txt`: Lists the Python dependencies.
- `.env`: Contains environment variables (not included in the repository).

## License
This project is licensed under the MIT License.
