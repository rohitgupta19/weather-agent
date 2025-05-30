import os
import requests
import boto3
from langchain_aws import BedrockLLM
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableSequence

def get_weather(city_name):
    """Fetch weather data for a given city using the Weather API."""
    api_key = os.getenv("WEATHER_API_KEY")
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric"
    }
    print(f"params : {params}")
    response = requests.get(base_url, params=params)
    print(f"response from the API : {response}")
    if response.status_code == 200:
        data = response.json()
        temperature = f"{data['main']['temp']:.2f}°C"
        country = data['sys'].get('country', 'Unknown')
        return f"The weather in {city_name}, {country} is {data['weather'][0]['description']} with a temperature of {temperature}. (Data provided by OpenWeatherMap API)"
    else:
        return f"Could not fetch weather data for {city_name}. Please check the city name. (Data provided by OpenWeatherMap API)"


def is_valid_city(location: str) -> bool:
    try:
        api_key = os.getenv("WEATHER_API_KEY")
        response = requests.get(
            "http://api.openweathermap.org/data/2.5/weather",
            params={
                "q": location,
                "appid": api_key
            },
            timeout=5
        )
        data = response.json()
        return data.get("cod") == 200
    except Exception:
        return False

def process_query(user_input):
    """Process the user input to extract city name (and country if provided) and fetch weather data."""
    bedrock_client = boto3.client(
        service_name="bedrock-runtime",
        region_name=os.getenv("AWS_REGION"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN")
    )

    bedrock = BedrockLLM(
        model="anthropic.claude-v2",
        client=bedrock_client
    )

    prompt = PromptTemplate(
        input_variables=["user_input"],
        template="""
        You are an AI assistant. Your task is based on the type of the input:

        1. If the input is a **weather-related question** (contains keywords like "weather", "temperature", "forecast", "climate", etc.), **extract and return only the city and country (if mentioned)** in the format:
        - "City,Country" (if country is included)
        - "City" (if country is not included)

        2. If the input is about **distance between cities**, provide:
        - The approximate road distance in kilometers
        - The typical driving time
        - A brief note about the main route

        3. If the input is any other type of question, provide a clear, accurate and direct answer based on your general knowledge.

        Input: {user_input}
        """
    )

    ai_agent = RunnableSequence(
        prompt | bedrock
    )

    ai_response = ai_agent.invoke({"user_input": user_input})
    print(f"AI Response: {ai_response}")
    if is_valid_city(ai_response.strip()):
        return get_weather(ai_response.strip())
    else:
        return ai_response
