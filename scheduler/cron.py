from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import asyncio


scheduler = AsyncIOScheduler()


async def monthly_plan_generation():
    
    """Run monthly content plan generation."""
    
    month = datetime.now().strftime("%B %Y")

    try:
        
        # Import here to avoid circular imports
        
        from api.routers.agent import generate_plan

        class Request:
            month = month

        result = await generate_plan(Request())
        print(f"Monthly plan generated: {result}")

    except Exception as e:
        print(f"Error in scheduled plan generation: {e}")


def start_scheduler():
    
    """Start the APScheduler."""
    # Schedule for 1st of month at 6:00 AM
    trigger = CronTrigger(day=1, hour=6, minute=0)

    scheduler.add_job(
        monthly_plan_generation,
        trigger=trigger,
        id="monthly_content_plan",
        name="Monthly Content Plan Generation",
    )

    scheduler.start()
    print("Scheduler started")


async def run_scheduler():
    """Run scheduler forever."""
    start_scheduler()
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        scheduler.shutdown()
        print("Scheduler stopped")
