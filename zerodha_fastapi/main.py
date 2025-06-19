from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from login_logic import get_login_url, generate_session
from positions import fetch_net_positions
from logger_config import setup_logger

app = FastAPI()
logger = setup_logger(__name__)
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login")
def login():
    return RedirectResponse(get_login_url())

@app.get("/callback")
def callback(request_token: str):
    try:
        generate_session(request_token)
        return HTMLResponse("<h3>Login successful!</h3><a href='/'>Back</a>")
    except Exception as e:
        return HTMLResponse(f"<h3>Error: {e}</h3><a href='/'>Back</a>")

@app.get("/positions", response_class=HTMLResponse)
def show_positions(request: Request):
    try:
        positions = fetch_net_positions()
        return templates.TemplateResponse("index.html", {"request": request, "positions": positions})
    except Exception as e:
        return HTMLResponse(f"<h3>Error: {e}</h3><a href='/'>Back</a>")

@app.get("/manage/{symbol}", response_class=HTMLResponse)
def manage_position(request: Request, symbol: str):
    positions = fetch_net_positions()
    position = next((p for p in positions if p["tradingsymbol"] == symbol), None)
    if not position:
        return HTMLResponse("<h3>Position not found</h3><a href='/positions'>Back</a>")
    return templates.TemplateResponse("manage.html", {"request": request, "position": position})

@app.post("/action")
def handle_action(symbol: str = Form(...), action: str = Form(...)):
    # Placeholder logic - implement your own logic here
    logger.info(f"Action '{action}' triggered on symbol: {symbol}")
    return RedirectResponse(f"/manage/{symbol}", status_code=303)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
