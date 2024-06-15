from typing import Dict
import os
from pathlib import Path
from datetime import datetime

# Set logging directory
current_dir = Path(__file__).absolute().parent.parent
logs_file_path = current_dir / "logs"

def get_time_now() -> str:
    """return date and time now

    Returns:
        str: the formatted date and time
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")



class FatehLogger:
    
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.logging_path = logs_file_path
            self.logs_file = os.path.join(self.logging_path, "fateh-logs.log")
            self.error_file = os.path.join(self.logging_path, "fateh-errors.log")
            self.initialized = True            
            self.log("INFO", f"Logger get initialized: {self}", __file__)


    def log(self, level: str, message: str, src: str = str(__file__)) -> None:
        try:
            if not os.path.isdir(self.logging_path):
                os.mkdir(self.logging_path)
            with open(self.logs_file, "a", encoding="utf-8") as log_file:
                logging_level = f"{level.upper():<9}"
                formatted_message = f"{get_time_now()} [{logging_level}] :: [{src}] : {message}\n"
                log_file.write(formatted_message)
        except FileNotFoundError as file_not_found:
            self.log_error(file_not_found)
            
        
    def log_error(self, message: str, src: str = str(__file__)) -> None:
        try:
            if not os.path.isdir(self.logging_path):
                os.mkdir(self.logging_path)
            with open(self.error_file, "a", encoding="utf-8") as log_file:
                level = "ERROR"
                logging_level = f"{level.upper():<9}"
                formatted_message = f"{get_time_now()} [{logging_level}] :: [{src}] : {message}\n"
                log_file.write(formatted_message)
        except FileNotFoundError as file_not_found:
            raise Exception (f"Exception occurred while logging to error.log file: {file_not_found}")

if __name__ == "__main__":
    logger = FatehLogger()