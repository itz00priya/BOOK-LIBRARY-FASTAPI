import asyncio
import traceback
from app.main import app, lifespan

async def run():
    try:
        async with lifespan(app):
            print("Successfully entered lifespan context")
    except Exception as e:
        print("Error entering lifespan context")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run())
