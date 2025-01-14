from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from logger.logger_factory import LoggerFactory
from dotenv import load_dotenv
import os

def setup():
    script_path = os.path.dirname(os.path.abspath(__file__))
    root_path = os.path.dirname(script_path)
    current_day = datetime.now().strftime("%Y%m%d")
    

    
    env_path = os.path.join(root_path, '.env')
    load_dotenv(env_path)

    key = os.path.join(root_path, 'account_service.json')
    LoggerFactory.info(f"Main :: Carregando conta de serviço :: GOOGLE_APPLICATION_CREDENTIALS :: {key}")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key

if __name__ == "__main__":
    setup()
