from datetime import datetime
import logging, os

class LoggerFactory:
    
    def __init__(self):
        current_day = datetime.now().strftime("%Y%m%d")

        self.logger = logging.getLogger(__name__)

        try:os.mkdir("logs")
        except:pass

        logging.basicConfig(
            filename = f"logs/LOG_{current_day}.log", 
            level = logging.INFO, 
            format = '%(asctime)s - %(levelname)s - %(message)s',
            encoding='UTF-8'
        )

    def info(self, msg: str):
        self.logger.info(msg)
        print(f'{datetime.now().replace(microsecond=0)} :: {msg}')
    
    def error(self, msg: str):
        self.logger.error(msg)
        print(f'{datetime.now().replace(microsecond=0)} :: {msg}')

    def __repr__(self) -> logging:
        self.logger