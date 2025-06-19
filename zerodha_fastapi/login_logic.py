import os
from dotenv import load_dotenv, set_key
from kiteconnect import KiteConnect
from logger_config import setup_logger

logger = setup_logger(__name__)
ENV_PATH = ".env"
load_dotenv(ENV_PATH)

API_KEY = os.getenv("ZERODHA_API_KEY")
API_SECRET = os.getenv("ZERODHA_API_SECRET")

kite = KiteConnect(api_key=API_KEY)

def get_login_url():
    return kite.login_url()

def generate_session(request_token):
    data = kite.generate_session(request_token, api_secret=API_SECRET)
    access_token = data["access_token"]
    kite.set_access_token(access_token)

    # Save tokens to .env
    set_key(ENV_PATH, "REQUEST_TOKEN", request_token)
    set_key(ENV_PATH, "ACCESS_TOKEN", access_token)
    logger.info("Access token stored")

    return access_token
