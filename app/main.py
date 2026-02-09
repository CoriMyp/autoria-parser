import aiohttp
import asyncio
import random
import os
import subprocess
from datetime import datetime, timedelta

from parser import process_page, process_all_autos
from db import init_db, save_autos
from config import settings
import api


def create_db_dump():
	print("Creating database dump..")
	os.makedirs("dumps", exist_ok=True)
	
	timestamp = datetime.now().strftime("%Y-%m-%d")
	filename = f"dumps/db_backup_{timestamp}.sql"
	
	env = os.environ.copy()
	env["PGPASSWORD"] = settings.POSTGRES_PASSWORD
	
	command = [
		"pg_dump",
		"-h", settings.POSTGRES_HOST,
		"-U", settings.POSTGRES_USER,
		"-d", settings.POSTGRES_DB,
		"-f", filename
	]
	
	try:
		subprocess.run(command, env=env, check=True)
		print(f"Dump saved to {filename}")
	except Exception as e:
		print(f"Failed to create DB dump: {e}")


async def run_parser():
	await init_db()
	api.init_semaphore(max_concurrent=5)
	
	total_processed_cars = 0
	
	async with aiohttp.ClientSession() as session:
		for page_num in range(settings.PAGES_COUNT):
			if settings.CARS_COUNT and total_processed_cars >= settings.CARS_COUNT:
				print(f"Reached limit of {settings.CARS_COUNT} cars. Stopping.")
				break

			print(f"--- Processing page {page_num} ---")

			auto_ids = await process_page(session, page_num)
			
			if not auto_ids:
				print(f"No autos found on page {page_num} (or error). Skipping.")
				await asyncio.sleep(5)
				continue

			print(f"Found {len(auto_ids)} autos. Fetching details...")

			autos = await process_all_autos(session, auto_ids)
			await save_autos(autos)
			total_processed_cars += len(autos)
			print(f"Parsed {len(autos)} autos from page {page_num}. Total: {total_processed_cars}")

			delay = random.uniform(2.0, 5.0)
			print(f"Sleeping for {delay:.2f} seconds...")
			await asyncio.sleep(delay)


async def main():
	print(f"Scheduler started. Target time: {settings.TIME_HOURS:02d}:{settings.TIME_MINS:02d}")

	await run_parser()
	
	# while True:
	# 	now = datetime.now()
	# 	target_time = now.replace(hour=settings.TIME_HOURS, minute=settings.TIME_MINS, second=0, microsecond=0)
		
	# 	if target_time <= now:
	# 		# Если время запуска на сегодня уже прошло, планируем на завтра
	# 		target_time += timedelta(days=1)
			
	# 	wait_seconds = (target_time - now).total_seconds()
	# 	print(f"Next run scheduled for {target_time} (in {wait_seconds/3600:.2f} hours)")
		
	# 	await asyncio.sleep(wait_seconds)
	# 	create_db_dump()
	# 	await run_parser()


if __name__ == "__main__":
	asyncio.run(main())
