import schedule
import time
import threading
import asyncio
from datetime import datetime

def run_news_collection(aggregator):
    """Run news collection in async context"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        loop.run_until_complete(aggregator.collect_and_process_news())
        print(f"News collection completed at {datetime.now()}")
    except Exception as e:
        print(f"Error during news collection: {e}")
    finally:
        loop.close()

def schedule_job(aggregator):
    """Schedule the daily news collection job"""
    schedule.every().day.at("06:00").do(run_news_collection, aggregator)
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

def start_scheduler(aggregator):
    """Start the scheduler in a separate thread"""
    scheduler_thread = threading.Thread(target=schedule_job, args=(aggregator,), daemon=True)
    scheduler_thread.start()
    
    # Run initial collection
    initial_thread = threading.Thread(target=run_news_collection, args=(aggregator,), daemon=True)
    initial_thread.start()
    
    print("News aggregation scheduler started - will run daily at 6:00 AM")