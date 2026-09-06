from fastapi import FastAPI  , Request 
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import requests
import os 

load_dotenv()

app = FastAPI(
    title="Custom NewsAPI"
)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name= "static"
)

templates = Jinja2Templates(directory="templates")

@app.get('/')
def index(request: Request, query: str = "latest"):
    # Fetch news from NewsAPI
    news_response = requests.get(
        url=f"https://newsapi.org/v2/everything?q={query}&apiKey={os.getenv('NEWS_API_KEY')}"
    )
    news_data = news_response.json()
    articles = news_data.get("articles", [])

    # Return a TemplateResponse, NOT a Jinja2Templates instance
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "query": query,
            "articles": articles,
        }
    )