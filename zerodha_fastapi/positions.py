import os
from dotenv import load_dotenv
from kiteconnect import KiteConnect
from logger_config import setup_logger

logger = setup_logger(__name__)
ENV_PATH = ".env"
load_dotenv(ENV_PATH)

def fetch_net_positions():
    api_key = os.getenv("ZERODHA_API_KEY")
    access_token = os.getenv("ACCESS_TOKEN")

    if not api_key or not access_token:
        logger.error("Missing credentials")
        raise ValueError("API key or access token missing")

    kite = KiteConnect(api_key=api_key)
    kite.set_access_token(access_token)

    logger.info("Fetching positions")
    return kite.positions()["net"]
