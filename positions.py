import os
from typing import Dict, Any
from kiteconnect import KiteConnect
from dotenv import load_dotenv
from logger_config import setup_logger

# Setup logger
logger = setup_logger(__name__)

class ZerodhaPositions:
    """Handles fetching Zerodha positions via KiteConnect."""

    def __init__(self, env_path: str = ".env"):
        logger.info("Initializing ZerodhaPositions with env_path: %s", env_path)
        try:
            load_dotenv(env_path)
            self.api_key = os.getenv("ZERODHA_API_KEY")
            self.access_token = os.getenv("ACCESS_TOKEN")

            if not self.api_key or not self.access_token:
                logger.error("Missing API key or access token in environment variables.")
                raise ValueError("API key or access token not found in .env file.")

            self.kite = KiteConnect(api_key=self.api_key)
            self.kite.set_access_token(self.access_token)
            logger.info("KiteConnect initialized with API key: %s", self.api_key[:4] + "****")

        except Exception as e:
            logger.error("Failed to initialize KiteConnect: %s", str(e))
            raise

    def fetch_positions(self) -> Dict[str, Any]:
        """Fetch positions from Zerodha Kite API."""
        logger.info("Fetching positions from Kite API")
        try:
            positions = self.kite.positions()
            logger.info("Fetched %d net positions", len(positions.get("net", [])))
            return positions["net"]
        except Exception as e:
            logger.error("Error fetching positions: %s", str(e))
            raise

def get_positions(env_path: str = ".env") -> Dict[str, Any]:
    """Convenience function to fetch net positions."""
    logger.info("Starting get_positions with env_path: %s", env_path)
    try:
        handler = ZerodhaPositions(env_path)
        return handler.fetch_positions()
    except Exception as e:
        logger.error("Failed to get positions: %s", str(e))
        raise

if __name__ == "__main__":
    logger.info("Starting main execution")
    try:
        net_positions = get_positions()
        logger.info("Retrieved %d net positions", len(net_positions))
        print("Net Positions:")
        for position in net_positions:
            print(position)
    except Exception as e:
        logger.error("Execution failed: %s", str(e))
        print(f"Failed to fetch positions: {str(e)}")
