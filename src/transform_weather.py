from pathlib import Path
import json
import csv
from datetime import datetime

from logger import get_logger  # ✅ use your logger

logger = get_logger("transform")  # ✅ create logger


BRONZE_DIR = Path("data/bronze")
SILVER_DIR = Path("data/silver")


def get_latest_bronze_file():
    if not BRONZE_DIR.exists():
        logger.error(f"{BRONZE_DIR} NOT FOUND")
        raise FileNotFoundError(f"{BRONZE_DIR} NOT FOUND")

    files = list(BRONZE_DIR.glob("*.json"))
    if not files:
        logger.error("No JSON file found in bronze layer")
        raise FileNotFoundError("No JSON file found")

    latest = max(files, key=lambda f: f.stat().st_mtime)
    logger.info(f"Using bronze file: {latest.name}")

    return latest


def load_bronze_json(filepath):
    logger.info(f"Loading file: {filepath.name}")

    with open(filepath, "r") as f:
        data = json.load(f)

    logger.info("JSON loaded successfully")
    return data


def clean_weather(raw_json, city_name="edmonton"):
    logger.info("Starting data transformation")

    hourly = raw_json.get("hourly", {})
    times = hourly.get("time", [])
    temps = hourly.get("temperature_2m", [])

    logger.info(f"Columns found: {list(hourly.keys())}")
    logger.info(f"Times count: {len(times)}")
    logger.info(f"Temps count: {len(temps)}")

    if len(times) != len(temps):
        logger.error("Mismatch between time and temperature")
        raise ValueError("Mismatch between time and temp")

    rows = [
        {"timestamp": t, "temp": temp, "city": city_name}
        for t, temp in zip(times, temps)
    ]

    logger.info("Transformation completed")
    return rows


def save_to_silver(rows):
    SILVER_DIR.mkdir(parents=True, exist_ok=True)

    filename = f"clean_{datetime.now().date()}.csv"
    filepath = SILVER_DIR / filename

    logger.info(f"Saving to silver: {filepath.name}")

    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "temp", "city"])
        writer.writeheader()
        writer.writerows(rows)

    logger.info(f"File saved successfully: {filepath}")


def main():
    logger.info("🚀 Starting transformation step")

    try:
        bronze_file = get_latest_bronze_file()
        raw_json = load_bronze_json(bronze_file)

        rows = clean_weather(raw_json)
        logger.info(f"Rows created: {len(rows)}")

        save_to_silver(rows)

    except Exception as e:
        logger.error(f"❌ Transformation failed: {e}")


if __name__ == "__main__":
    main()