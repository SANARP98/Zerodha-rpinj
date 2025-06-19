import os
import http.server
import webbrowser
from kiteconnect import KiteConnect
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv, set_key
from logger_config import setup_logger

# Setup logging
logger = setup_logger(__name__)

# Load environment variables
ENV_PATH = ".env"
load_dotenv(ENV_PATH)

API_KEY = os.getenv("ZERODHA_API_KEY")
API_SECRET = os.getenv("ZERODHA_API_SECRET")

if not API_KEY or not API_SECRET:
    logger.error("API key or secret not found in .env file")
    raise ValueError("Missing API key or secret in .env file")

kite = KiteConnect(api_key=API_KEY)

# Step 1: Open login URL
login_url = kite.login_url()
logger.info(f"Opening login URL in browser: {login_url}")
webbrowser.open(login_url)

# Step 2: HTTP server to capture request_token
class TokenHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        query = urlparse(self.path).query
        params = parse_qs(query)
        request_token = params.get("request_token", [None])[0]
        if request_token:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Login successful! You may close this tab.")
            logger.info(f"Received request token: {request_token}")

            # Step 3: Exchange for access token
            try:
                data = kite.generate_session(request_token, api_secret=API_SECRET)
                access_token = data["access_token"]
                kite.set_access_token(access_token)
                logger.info(f"Generated access token: {access_token}")

                # Step 4: Write tokens to .env
                set_key(ENV_PATH, "REQUEST_TOKEN", request_token)
                set_key(ENV_PATH, "ACCESS_TOKEN", access_token)
                logger.info("Tokens written to .env file")
            except Exception as e:
                logger.error(f"Failed to generate session: {str(e)}")
                self.wfile.write(f"Error: {str(e)}".encode())
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Request token not found.")
            logger.error("Request token not found in redirect URL")

# Start server
logger.info("Starting HTTP server on http://localhost:8000...")
server = http.server.HTTPServer(("localhost", 8000), TokenHandler)
try:
    server.handle_request()
except Exception as e:
    logger.error(f"Server error: {str(e)}")
