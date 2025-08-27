import asyncio
import logging
from bot import bot, dp
from database import create_tables

logging.basicConfig(level=logging.INFO)

async def main():
    await create_tables()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())