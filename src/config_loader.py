from pathlib import Path
import json
from logger import get_logger

logger = get_logger(__name__)

CONFIG_PATH = Path("config/config.json")


def load_config(config_path: Path = CONFIG_PATH) -> dict:
    """Load configuration from JSON file."""

    if not config_path.exists():
        logger.error(f"Config file not found: {config_path}")
        raise FileNotFoundError(config_path)

    logger.info(f"Loading config from {config_path}")

    try:
        with open(config_path, "r") as f:
            config = json.load(f)

        logger.info("Config loaded successfully")
        return config

    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON format: {e}")
        raise