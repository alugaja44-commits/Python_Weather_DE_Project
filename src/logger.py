import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from datetime import datetime

def get_logger(name:str)->logging.Logger:
    log_dir=Path("logs")        
    log_dir.mkdir(exist_ok=True)
    log_file=log_dir/f"{datetime.now():%Y-%m-%d}.log"
    logger=logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # check if handlers already exist. prevent dulpicate logs
    if not logger.handlers:
        #write to file.creating logging system
        file_handler=RotatingFileHandler(log_file,maxBytes=1_000_000,backupCount=3)

        # logs to terminal
        console_handler=logging.StreamHandler()

        formatter=logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
        #apply format
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        #Attach handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
    




