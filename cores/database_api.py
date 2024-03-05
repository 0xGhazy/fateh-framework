import sqlite3
from pathlib import Path
import os
from typing import Dict, List, Optional, Tuple
from cores.fateh_logger import FatehLogger


# Set database directory
current_dir = Path(__file__).absolute().parent
database_path = current_dir / "database.db"

class DatabaseAPI:
    _instance = None

    def __new__(cls, logger: FatehLogger):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


    def __init__(self, logger: FatehLogger):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.database_path = database_path
            self.logger = logger
            self.logger.log("INFO", "Database Logger injected successfully", __file__)
            self.connection = self._connect()
            self.cursor = self.connection.cursor()


    def _connect(self) -> Optional[sqlite3.Connection | None]:
        try:
            connection = sqlite3.connect(self.database_path)
            self._db_log("INFO", f"Database connected successfully @ [{self.database_path}] | {connection}")
            return connection
        except sqlite3.Error as error:
            self._db_log("EXCEPTION", f"Error occurred while connecting to database: {str(error)}")
            
    
    def is_connected(self) -> bool:
        if self.connection is not None:
            return True
        return False
    
    
    def _db_log(self, level, message):
        if self.logger is not None:
            self.logger.log(f"{level}", message, str(__file__))
        

    def load_configurations(self) -> Dict:
        configurations = {}
        try:
            result = self.cursor.execute("SELECT property, value FROM configurations;")
            for row in result:
                configurations[row[0]] = row[1]
            if configurations:
                self._db_log("INFO", f"Configurations are loaded successfully [{len(configurations)}] record")
        except Exception as e:
            self._db_log("EXCEPTION", f"Error occurred while loading configurations: {e}")
        return configurations


    def insert_client(self, client: Tuple) -> bool:
        try:
            self.cursor.execute(f"""INSERT INTO clients (name, ip, port, sys_arch, security_solution)
                    VALUES (?, ?, ?, ?, ?);""", client)
            self.connection.commit()
            self._db_log("INFO", f"""INSERT INTO clients (name, ip, port, sys_arch, security_solution) VALUES (?, ?, ?, ?, ?); ({client})""")
            return True
        except sqlite3.IntegrityError as integrity_error:
            constraint_failed_in = str(integrity_error).split(": ")[1]
            self._db_log("EXCEPTION", f"IntegrityError occurred while insertion with client: {client} | Error message: {constraint_failed_in}")
            return False


if __name__ == "__main__":
    x = DatabaseAPI()