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
        template="You are an AI assistant. Extract only the city name and country (if provided) from the following input: {user_input}. Return them in the format 'City,Country' or just 'City' if no country is provided."
    )

    ai_agent = RunnableSequence(
        prompt | bedrock
    )

    ai_response = ai_agent.invoke({"user_input": user_input})
    location = ai_response.strip()

    if location.lower() in user_input.lower():
        city_name = location.split(',')[0].strip()
    else:
        raise ValueError("Failed to extract a valid city name from the input.")

    return get_weather(location)
