"""
Build a single AI agents with use of custom Tools implemented locally.
The Agent get the weather condition from local IP Address and write it to a text file.

Three Tools are involved:
    1. get_weather_from_ip
    2. get_current_time
    3. write_txt_file

"""

import aisuite as ai
import requests
import os
from datetime import datetime
from loguru import logger


def get_output_paths():
 # Get this script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Get the script name
    script_name = os.path.basename(__file__).split(".")[0]
    outut_dir = os.path.join(script_dir, "data", "output")
    os.makedirs(outut_dir, exist_ok=True)
    return outut_dir, script_name
    
def get_current_time():
    """
    Returns the current time as a string.
    """
    return datetime.now().strftime("%H:%M:%S")

"""
tools = [{
    "type": "function",
    "function": {
        "name": "get_current_time", # <--- Your functions name
        "description": "Returns the current time as a string.", # <--- a description for the LLM
        "parameters": {}
    }
}]
"""


def get_weather_from_ip():
    """
    Gets the current, high, and low temperature in Fahrenheit for the user's
    location and returns it to the user.
    """
    loc_response = requests.get('https://ipinfo.io/json').json()
    logger.debug(loc_response)
    # Get location coordinates from the IP address
    lat, lon = loc_response['loc'].split(',')

    # Set parameters for the weather API call
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m",
        "daily": "temperature_2m_max,temperature_2m_min",
        "temperature_unit": "celsius",
        "timezone": "auto"
    }

    # Get weather data
    weather_data = requests.get("https://api.open-meteo.com/v1/forecast", params=params).json()

    # get Today's date
    today_date = datetime.now().strftime("%Y-%m-%d")

    # Format and return the simplified string
    return (
        f"Country: {loc_response['country']}, "
        f"City: {loc_response['region']}, "
        f"Date: {today_date}, "
        f"Current: {weather_data['current']['temperature_2m']}°C, "
        f"High: {weather_data['daily']['temperature_2m_max'][0]}°C, "
        f"Low: {weather_data['daily']['temperature_2m_min'][0]}°C"
    )

# Write a text file
def write_txt_file(file_name: str, content: str):
    """
    Write a string into a .txt file (overwrites if exists).
    Args:
        file_path (str): Name of the output file with ".txt" extension.
        content (str): Text to write.
    Returns:
        str: Path to the written file.
    """
    output_dir, output_prefix = get_output_paths()

    file_path = f"{output_dir}/{output_prefix}_{file_name}"
   
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    return file_path


### MAIN ###
if __name__ == "__main__":

    # Create an instance of the AISuite client
    client = ai.Client()
   
    prompt = "Also write me a txt note with the current weather please in Celsuis. Specify the date, city and country name."

    response = client.chat.completions.create(
        model="openai:o4-mini",
        messages=[{"role": "user", "content": (
            prompt
        )}],
        tools=[
            get_weather_from_ip,
            get_current_time,
            write_txt_file
        ],
        max_turns= 5 # limit the number of turns to 5
    )

    logger.info(response)