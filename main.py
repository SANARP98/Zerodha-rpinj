from logger_config import setup_logger
from positions import get_positions

# Setup logger
logger = setup_logger(__name__)

def main():
    try:
        net_positions = get_positions()
        logger.info("Net Positions Retrieved:")
        for position in net_positions:
            print(position)
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")

if __name__ == "__main__":
    main()
