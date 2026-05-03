import subprocess
import sys
from datetime import datetime
from logger import get_logger
from config_loader import load_config
logger = get_logger(__name__)
config = load_config()

def run_step(description: str, command: list[str]) -> bool:
    """
    Run a single pipeline step as a subprocess.
    Returns True if the step succeeded, False otherwise.
    """
    logger.info("Starting step: %s", description)
    print(f"\n=== {description} ===")
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False
        )
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        if result.returncode == 0:
            logger.info("Step succeeded: %s", description)
            print(f"✅ Step succeeded: {description}")
            return True
        logger.error("Step failed (%s): return code %s", description, result.returncode)
        print(f"❌ Step failed: {description}")
        return False
    except Exception as e:
        logger.exception("Exception while running step: %s", description)
        print(f"❌ Exception running step {description}: {e}")
        return False

def main():
    logger.info("Full pipeline run started")
    start_time = datetime.now()
    print(f"\n🚀 Pipeline started at {start_time}\n")
    steps = [
        ("Fetch Weather into Bronze", ["python", "src/fetch_weather.py"]),
        ("Transform Bronze Silver", ["python", "src/transform_weather.py"]),
        ("Convert Silver Parquet Gold", ["python", "src/to_parquet.py"]),
        ("Load Silver into SQLite", ["python", "src/load_to_sql.py"]),
    ]
    all_success = True
    for desc, cmd in steps:
        success = run_step(desc, cmd)
        if not success:
            all_success = False
            logger.warning("Aborting pipeline due to failure in step: %s", desc)
            break
    end_time = datetime.now()
    duration = end_time - start_time
    if all_success:
        logger.info("Pipeline finished successfully in %s seconds", duration.total_seconds())
        print(f"\n🎉 Pipeline completed successfully in {duration}\n")
    else:
        logger.error("Pipeline ended with errors after %s seconds", duration.total_seconds())
        print(f"\n⚠️ Pipeline ended with errors in {duration}\n")

if __name__ == "__main__":
    main()
