import requests
import json
import logging
from datetime import datetime
import os
from logger import get_logger

logger=get_logger("weather")

def fetch_weather():
    url=("https://api.open-meteo.com/v1/forecast?latitude=53.55&longitude=-113.46&hourly=temperature_2m")
    logger.info("caling weather API")

    try:
        response=requests.get(url,timeout=10)
        response.raise_for_status()
        data=response.json()
        logger.info("API Call successful")
        return data
    except Exception as e:
        logger.error(f"{datetime.now()}- API error :{e}")
        print(e)
        return None
def save_to_bronze(data):
    os.makedirs("data/bronze",exist_ok=True)
    filename=datetime.now().strftime("%Y-%m-%d.json")
    filepath=os.path.join("data/bronze",filename)
    try:
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

        logger.info(f" Raw weather saved to {filepath}")

    except Exception as e:
        logger.error(f" Failed to save data: {e}")

def main():
    logger.info(" Starting weather pipeline (fetch step)")

    weather=fetch_weather()
    
    if weather :
        save_to_bronze(weather)
    else:
        logger.warning(" No data received from API")



if __name__ == "__main__":
    main()
    