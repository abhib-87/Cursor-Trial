from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from datetime import datetime
import json
import os
from news_aggregator import NewsAggregator
from scheduler import start_scheduler

app = FastAPI(title="Automotive News Aggregator", version="1.0.0")

# Mount static files and templates
os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize news aggregator
aggregator = NewsAggregator()

@app.on_event("startup")
async def startup_event():
    """Start the scheduler when the app starts"""
    start_scheduler(aggregator)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Main page showing aggregated news"""
    try:
        # Load latest news data
        news_data = aggregator.get_latest_news()
        return templates.TemplateResponse(
            "index.html", 
            {
                "request": request, 
                "news_data": news_data,
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "index.html", 
            {
                "request": request, 
                "news_data": {"error": str(e)},
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        )

@app.get("/api/news")
async def get_news():
    """API endpoint to get latest news data"""
    return aggregator.get_latest_news()

@app.post("/api/refresh")
async def refresh_news():
    """API endpoint to manually refresh news"""
    try:
        await aggregator.collect_and_process_news()
        return {"status": "success", "message": "News refreshed successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)