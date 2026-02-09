import asyncio
import json
import logging

import config


logger = logging.getLogger(__name__)


semaphore: asyncio.Semaphore | None = None

def init_semaphore(max_concurrent: int = 5) -> None:
	global semaphore
	semaphore = asyncio.Semaphore(max_concurrent)


async def fetch_page(session, page_num: int):
	if semaphore is None:
		init_semaphore()
	
	async with semaphore:
		params = {
			"page": page_num,
			"device": "desktop-web",
			"onlyItems": 1,
			"limit": 100
		}
		try:
			async with session.get("https://auto.ria.com/bff/search/public/search", params=params) as response:
				if response.status != 200:
					logger.error(f"Error fetching page {page_num}: Status {response.status}")
					return None
				return await response.json()
		except Exception as e:
			logger.error(f"Exception in fetch_page {page_num}: {e}")
			return None


async def fetch_auto(session, auto_id: int, url: str):
	if semaphore is None:
		init_semaphore()
	
	async with semaphore:
		params = {
			"langId": "4",
			"device": "desktop-web",
			"ssr": "0",
			"hash": "b08efe77e20c54eb88bb7992927c50a8",
		}
		headers = config.HEADERS.copy()
		headers["Referer"] = url
		try:
			async with session.get(f"https://auto.ria.com/bff/final-page/public/{auto_id}",
							   	headers=headers, params=params) as response:
				if response.status != 200:
					logger.error(f"Error fetching auto {auto_id}: Status {response.status}")
					return None
				return await response.json()
		except Exception as e:
			logger.error(f"Exception in fetch_auto {auto_id}: {e}")
			return None
	

async def fetch_phone(session, auto_id: int, phone_data: list):
	if semaphore is None:
		init_semaphore()
	
	async with semaphore:
		body = {
			"blockId": "autoPhone",
			"autoId": auto_id,
			"data": phone_data
		}
		try:
			async with session.post("https://auto.ria.com/bff/final-page/public/auto/popUp/",
								headers=config.HEADERS, json=body) as response:
				if response.status != 200:
					logger.error(f"Error fetching phone for {auto_id}: Status {response.status}")
					return None
				return await response.json()
		except Exception as e:
			logger.error(f"Exception in fetch_phone {auto_id}: {e}")
			return None
